import logging
import re
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from openg2p_registry_core.models import G2PRegisterChangeRequest
from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_lifecycle_utils import (
    apply_approval, current_stage, mark_pending, stage_for_section,
)
from .domain_validation_utils import as_float, as_int, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


_MOBILE_NUMBER_PATTERN = re.compile(r"^\+?[0-9][0-9\- ]{5,19}$")

# Farmer ids are issued by the farmer registry as FR- followed by ten digits.
_FARMER_ID_PATTERN = re.compile(r"^FR-[0-9]{10}$")

class G2PRegisterDomainServiceCropSown(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_production_year(record)
            self._validate_farmer_id(record)

    def _validate_production_year(self, record: dict) -> None:
        year = as_int(record.get("production_year"))
        if year is not None and year > date.today().year:
            validation_error("production_year must not be in the future")


    def _validate_farmer_id(self, record: dict) -> None:
        """Farmer ids come from the farmer registry as FR- plus ten digits."""
        value = record.get("farmer_id")
        if value is None or str(value).strip() == "":
            return
        if not _FARMER_ID_PATTERN.match(str(value).strip()):
            validation_error(
                f"farmer_id must be FR- followed by 10 digits (got '{value}')"
            )

    def _validate_mobile_number(self, record: dict, field: str) -> None:
        value = record.get(field)
        if value is None or str(value).strip() == "":
            return
        if not _MOBILE_NUMBER_PATTERN.match(str(value).strip()):
            validation_error(f"{field} is not a valid mobile number")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for crop sown record")

        keys = [
            "functional_record_id",
            "farmer_name",
            "farmer_id",
            "fayda_fan_id",
            "status",
            "production_year",
            "lifecycle_stage",
            "region",
            "zone",
            "woreda",
            "kebele",
            "latitude",
            "longitude",
            "address_line_1",
            "address_line_2",
            "postal_code",
            "country_code",
        ]
        search_text = []
        if extra:
            search_text.extend(str(item).strip() for item in extra if str(item).strip())
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(search_text).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for crop sown record")

        keys = ["farmer_id"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()

    # ── Cross-record rules ──────────────────────────────────────────────────
    # `validate_domain_attributes` only sees the records being written, so rules
    # that span a record and its siblings cannot live there. `pre_approve` runs
    # on approval with a live session, which is the first point both the record
    # and the database are available — so the Odoo @api.constrains that query
    # other rows are enforced here.

    async def pre_approve(self, change_request: G2PRegisterChangeRequest, session: AsyncSession):
        await self._check_unique_farmer_per_year(change_request, session)
        await self._check_crop_area_within_plot(change_request, session)
        await self._refresh_admin_names(change_request, session)
        await self._adopt_uploaded_photo(change_request, session)

    async def _adopt_uploaded_photo(
        self, change_request: G2PRegisterChangeRequest, session: AsyncSession
    ) -> None:
        """Promote a photo uploaded on the form to the record's avatar.

        A file widget stores its upload as a *section document* — the submit
        flow posts `documents: [{document_id, label}]` and never touches
        `record_image_document_id`, which is the field the profile widget and
        the record tree read. So an uploaded photo is saved but invisible.

        This bridges the two: on approval, if the record has no avatar yet, the
        earliest image attached to it becomes one. Records that already have an
        avatar are left alone, so re-approving cannot swap someone's photo.
        """
        from openg2p_registry_core.models import (
            G2PRegisterSectionDocument,
            G2PRegistryDocument,
        )

        from ..models import G2PRegisterCropSown

        record = await session.get(G2PRegisterCropSown, change_request.internal_record_id)
        if record is None or record.record_image_document_id:
            return

        row = (
            await session.execute(
                select(G2PRegistryDocument)
                .join(
                    G2PRegisterSectionDocument,
                    G2PRegisterSectionDocument.document_id
                    == G2PRegistryDocument.document_id,
                )
                .where(
                    G2PRegisterSectionDocument.internal_record_id
                    == change_request.internal_record_id
                )
                .where(G2PRegistryDocument.bucket == "documents")
                .order_by(G2PRegistryDocument.created_at)
            )
        ).scalars().first()

        if row is not None and self._is_image(row.source_filename):
            record.record_image_document_id = row.document_id

    @staticmethod
    def _is_image(filename: str | None) -> bool:
        return str(filename or "").lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp", ".gif")
        )

    async def _refresh_admin_names(
        self, change_request: G2PRegisterChangeRequest, session: AsyncSession
    ) -> None:
        """Copy the admin unit display names onto the record.

        The register search returns stored values verbatim, so a tree column
        bound to `region` shows REGION_ET11. These denormalised names give the
        tree something readable while the coded value stays authoritative.
        """
        from sqlalchemy import text
        from sqlalchemy.ext.asyncio import async_sessionmaker
        from openg2p_registry_core.engine import get_engines
        from openg2p_registry_core.models import G2PAttributeValue

        from ..models import G2PRegisterCropSown

        record = await session.get(G2PRegisterCropSown, change_request.internal_record_id)
        if record is None:
            return
        for field, name_field in (("region", "region_name"), ("zone", "zone_name"),
                                  ("woreda", "woreda_name"), ("kebele", "kebele_name")):
            value_id = getattr(record, field, None)
            if not value_id:
                setattr(record, name_field, None)
                continue
            
            # 1. Try local attributes table first
            row = (
                await session.execute(
                    select(G2PAttributeValue).where(G2PAttributeValue.value_id == value_id)
                )
            ).scalars().first()
            display_name = getattr(row, "value_display", None) if row else None
            
            # 2. Fall back to master-data geo hierarchy values
            if not display_name:
                master_data_engine = get_engines().get("db_engine_master_data")
                if master_data_engine:
                    parts = value_id.split("_", 1)
                    geo_id = f"{parts[0].lower()}-{parts[1]}" if len(parts) > 1 else value_id
                    session_maker = async_sessionmaker(master_data_engine, expire_on_commit=False)
                    async with session_maker() as md_session:
                        md_row = (await md_session.execute(
                            text("SELECT display_name FROM g2p_geo_level_values WHERE level_value_id = :val_id OR level_value_id = :orig_id"),
                            {"val_id": geo_id, "orig_id": value_id}
                        )).fetchone()
                        if md_row:
                            display_name = md_row[0]
            
            setattr(record, name_field, display_name)


    async def _check_unique_farmer_per_year(
        self, change_request: G2PRegisterChangeRequest, session: AsyncSession
    ) -> None:
        """Odoo: `_check_unique_farmer_id` — one registration per farmer per
        production year."""
        from ..models import G2PRegisterCropSown

        record = await session.get(G2PRegisterCropSown, change_request.internal_record_id)
        if record is None or not record.farmer_id or not record.production_year:
            return

        clash = (
            await session.execute(
                select(func.count())
                .select_from(G2PRegisterCropSown)
                .where(
                    G2PRegisterCropSown.farmer_id == record.farmer_id,
                    G2PRegisterCropSown.production_year == record.production_year,
                    G2PRegisterCropSown.internal_record_id != record.internal_record_id,
                    G2PRegisterCropSown.record_status == "ACTIVE",
                )
            )
        ).scalar_one()
        if clash:
            validation_error(
                f"Farmer {record.farmer_id} already has a crop sown record for "
                f"{record.production_year}"
            )

    async def _check_crop_area_within_plot(
        self, change_request: G2PRegisterChangeRequest, session: AsyncSession
    ) -> None:
        """Odoo: `_check_land_area_allocation` / `_check_actual_crop_area_limits`.

        The crop area planned or worked on a plot may not exceed that plot's
        total area. Each line carries its own land_id and land_area, so the
        check groups a record's lines by plot and compares the sum against the
        area declared for it.
        """
        from ..models import (
            G2PRegisterCultivation, G2PRegisterPlanning, G2PRegisterSowing,
        )

        checks = [
            (G2PRegisterPlanning, "planned_area", "planned"),
            (G2PRegisterCultivation, "actual_crop_area", "cultivated"),
            (G2PRegisterSowing, "area_sown", "sown"),
        ]
        for model, area_field, label in checks:
            rows = (
                await session.execute(
                    select(model).where(
                        model.link_internal_record_id == change_request.internal_record_id,
                        model.record_status == "ACTIVE",
                    )
                )
            ).scalars().all()

            by_plot: dict[str, list] = {}
            for row in rows:
                key = getattr(row, "land_id", None) or getattr(row, "land_uuid", None)
                if key:
                    by_plot.setdefault(key, []).append(row)

            for plot, plot_rows in by_plot.items():
                total = sum(as_float(getattr(r, area_field, None)) or 0.0 for r in plot_rows)
                plot_area = next(
                    (as_float(r.land_area) for r in plot_rows if as_float(r.land_area)), None
                )
                if plot_area and total > plot_area + 1e-6:
                    validation_error(
                        f"Total {label} area on plot {plot} is {total:g} ha, which exceeds "
                        f"its registered area of {plot_area:g} ha"
                    )

    # ── Lifecycle ───────────────────────────────────────────────────────────
    # AWE owns the approval decision; the ladder is ours. `post_approve` runs
    # once a change request is approved, which is the moment Odoo's
    # action_approve_wah would have advanced the stage.

    async def post_approve(self, change_request: G2PRegisterChangeRequest, session: AsyncSession):
        from ..models import G2PRegisterCropSown

        record = await session.get(G2PRegisterCropSown, change_request.internal_record_id)
        if record is None:
            return

        section_mnemonic = await self._resolve_section_mnemonic(change_request, session)
        stage = stage_for_section(section_mnemonic) or current_stage(record)
        apply_approval(record, stage)
        _logger.info(
            "crop sown %s: %s approved, lifecycle now %s",
            record.internal_record_id, stage, record.lifecycle_stage,
        )

    async def pre_submit_stage(self, record, section_mnemonic: str) -> None:
        """Mark the stage pending when its section is submitted for approval."""
        stage = stage_for_section(section_mnemonic)
        if stage:
            mark_pending(record, stage)

    async def _resolve_section_mnemonic(
        self, change_request: G2PRegisterChangeRequest, session: AsyncSession
    ) -> str:
        from openg2p_registry_core.models import G2PRegisterSection

        if not change_request.section_id:
            return ""
        section = await session.get(G2PRegisterSection, change_request.section_id)
        return getattr(section, "section_mnemonic", "") or ""
