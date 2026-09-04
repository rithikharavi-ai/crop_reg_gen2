import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import as_float, parse_date, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceSowing(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict], session=None, **kwargs):
        for record in records:

            from .domain_validation_utils import validate_alphabetical_name, validate_mobile_number
            validate_alphabetical_name(record.get("farmer_name"), "Farmer Name")
            validate_alphabetical_name(record.get("da_name"), "DA Name")
            validate_alphabetical_name(record.get("supervisor_name"), "Supervisor Name")
            validate_mobile_number(record.get("da_mobile_number"), "DA Mobile Number")
            validate_mobile_number(record.get("supervisor_mobile_number"), "Supervisor Mobile Number")
            self._validate_sowing_date(record)
            self._validate_area_sown(record)
            self._validate_seed_quantity(record)
            if session:
                await self._validate_land_id_matches_planning(record, session=session)

    async def _validate_land_id_matches_planning(self, record: dict, session) -> None:
        land_id = record.get("land_id")
        if not land_id or not str(land_id).strip():
            return

        submission_id = record.get("submission_id")
        link_internal_record_id = record.get("link_internal_record_id")

        if not submission_id and not link_internal_record_id:
            return

        from sqlalchemy import text

        planning_land_ids = set()

        if submission_id:
            res = await session.execute(
                text("SELECT land_id FROM g2p_intake_form_plannings WHERE submission_id = :sub_id"),
                {"sub_id": submission_id}
            )
            for row in res.fetchall():
                if row[0] and str(row[0]).strip():
                    planning_land_ids.add(str(row[0]).strip())

        if link_internal_record_id:
            res = await session.execute(
                text("SELECT land_id FROM g2p_register_plannings WHERE link_internal_record_id = :rec_id AND record_status = 'ACTIVE'"),
                {"rec_id": link_internal_record_id}
            )
            for row in res.fetchall():
                if row[0] and str(row[0]).strip():
                    planning_land_ids.add(str(row[0]).strip())

        if str(land_id).strip() not in planning_land_ids:
            validation_error(f"Land ID '{land_id}' in Sowing does not match any Land ID specified in Crop Planning.")

    def _validate_sowing_date(self, record: dict) -> None:
        sowing_date = parse_date(record.get("sowing_date"))
        if sowing_date is not None and sowing_date > date.today():
            validation_error("sowing_date must not be in the future")

    def _validate_area_sown(self, record: dict) -> None:
        area_sown = as_float(record.get("area_sown"))
        if area_sown is not None and area_sown <= 0:
            validation_error("area_sown must be greater than zero when provided")

    def _validate_seed_quantity(self, record: dict) -> None:
        seed_qty = as_float(record.get("actual_seed_qty"))
        if seed_qty is not None and seed_qty < 0:
            validation_error("actual_seed_qty must not be negative")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for sowing")

        keys = [
            "functional_record_id",
            "land_id",
            "season",
            "commodity",
            "crop_variety",
            "crop_category",
            "sowing_status",
            "area_sown",
            "seed_class",
            "fertilizer_type",
            "cultivated_by",
            "cluster_status",
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
        _logger.info("Constructing record name for sowing")

        keys = ["commodity", "season", "area_sown"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
