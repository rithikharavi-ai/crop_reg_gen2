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
            self._validate_sowing_date(record)
            self._validate_area_sown(record)
            from .domain_compute_utils import compute_ec_date
            compute_ec_date(record, "sowing_date", "sowing_date_ec")
            if session:
                await self._validate_land_id_matches_planning(record, session=session)

    async def _validate_land_id_matches_planning(self, record: dict, session) -> None:
        land_id = record.get("land_id")
        if not land_id or not str(land_id).strip():
            return

        submission_id = record.get("submission_id")
        link_internal_record_id = record.get("link_internal_record_id")
        fayda_fan_id = record.get("fayda_fan_id")

        if not submission_id and not link_internal_record_id and not fayda_fan_id:
            return

        from sqlalchemy import text

        valid_land_ids = set()

        # 1. Check current submission intake tables for Planning and Cultivation
        if submission_id:
            res_p = await session.execute(
                text("SELECT land_id FROM g2p_intake_form_plannings WHERE submission_id = :sub_id"),
                {"sub_id": submission_id}
            )
            for row in res_p.fetchall():
                if row[0] and str(row[0]).strip():
                    valid_land_ids.add(str(row[0]).strip())

            res_c = await session.execute(
                text("SELECT land_id FROM g2p_intake_form_cultivations WHERE submission_id = :sub_id"),
                {"sub_id": submission_id}
            )
            for row in res_c.fetchall():
                if row[0] and str(row[0]).strip():
                    valid_land_ids.add(str(row[0]).strip())

            if not fayda_fan_id:
                res_f = await session.execute(
                    text("SELECT fayda_fan_id FROM g2p_intake_form_crop_sowns WHERE submission_id = :sub_id AND fayda_fan_id IS NOT NULL"),
                    {"sub_id": submission_id}
                )
                f_row = res_f.fetchone()
                if f_row and f_row[0]:
                    fayda_fan_id = f_row[0]

        # 2. Check registered DB records by link_internal_record_id or Fayda ID
        master_ids = set()
        if link_internal_record_id:
            master_ids.add(str(link_internal_record_id))

        if fayda_fan_id:
            res_m = await session.execute(
                text("SELECT internal_record_id::text FROM g2p_register_crop_sowns WHERE fayda_fan_id = :fayda AND record_status = 'ACTIVE'"),
                {"fayda": fayda_fan_id}
            )
            for row in res_m.fetchall():
                if row[0]:
                    master_ids.add(str(row[0]))

        if master_ids:
            res_db_p = await session.execute(
                text("SELECT land_id FROM g2p_register_plannings WHERE link_internal_record_id = ANY(:m_ids) AND record_status = 'ACTIVE'"),
                {"m_ids": list(master_ids)}
            )
            for row in res_db_p.fetchall():
                if row[0] and str(row[0]).strip():
                    valid_land_ids.add(str(row[0]).strip())

            res_db_c = await session.execute(
                text("SELECT land_id FROM g2p_register_cultivations WHERE link_internal_record_id = ANY(:m_ids) AND record_status = 'ACTIVE'"),
                {"m_ids": list(master_ids)}
            )
            for row in res_db_c.fetchall():
                if row[0] and str(row[0]).strip():
                    valid_land_ids.add(str(row[0]).strip())

        if str(land_id).strip() not in valid_land_ids:
            msg_fayda = f" for Fayda ID '{fayda_fan_id}'" if fayda_fan_id else ""
            validation_error(f"Land ID '{land_id}' in Sowing does not match any Land ID specified in Crop Planning or Cultivation{msg_fayda}.")

    def _validate_sowing_date(self, record: dict) -> None:
        sowing_date = parse_date(record.get("sowing_date"))
        if sowing_date is not None and sowing_date > date.today():
            validation_error("sowing_date must not be in the future")

    def _validate_area_sown(self, record: dict) -> None:
        area_sown = as_float(record.get("area_sown"))
        if area_sown is not None and area_sown <= 0:
            validation_error("area_sown must be greater than zero when provided")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for sowing")

        keys = [
            "functional_record_id",
            "land_id",
            "season",
            "commodity",
            "crop_variety",
            "crop_category",
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
