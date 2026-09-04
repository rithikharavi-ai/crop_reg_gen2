import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_compute_utils import compute_ec_date
from .domain_validation_utils import as_float, parse_date, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceInfestation(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict], session=None, **kwargs):
        for record in records:

            from .domain_validation_utils import validate_alphabetical_name, validate_mobile_number
            validate_alphabetical_name(record.get("farmer_name"), "Farmer Name")
            validate_alphabetical_name(record.get("da_name"), "DA Name")
            validate_alphabetical_name(record.get("supervisor_name"), "Supervisor Name")
            validate_mobile_number(record.get("da_mobile_number"), "DA Mobile Number")
            validate_mobile_number(record.get("supervisor_mobile_number"), "Supervisor Mobile Number")
            self._validate_observation_date(record)
            self._validate_estimated_damage(record)
            compute_ec_date(record, "observation_date", "observation_date_ec")
            if session:
                await self._validate_land_id_matches_sowing(record, session=session)

    async def _validate_land_id_matches_sowing(self, record: dict, session) -> None:
        """
        Validates that the Land ID entered in Pest/Disease Infestation actually exists in the Sowing section.
        Since infestation occurs on already sown land, this ensures cross-section data integrity.
        """
        land_id = record.get("land_id")
        if not land_id or not str(land_id).strip():
            return

        submission_id = record.get("submission_id")
        link_internal_record_id = record.get("link_internal_record_id")

        if not submission_id and not link_internal_record_id:
            return

        from sqlalchemy import text

        sowing_land_ids = set()

        # 1. Fetch Land IDs saved in intake form sowings for this submission (Pending CRs)
        if submission_id:
            res = await session.execute(
                text("SELECT land_id FROM g2p_intake_form_sowings WHERE submission_id = :sub_id"),
                {"sub_id": submission_id}
            )
            for row in res.fetchall():
                if row[0] and str(row[0]).strip():
                    sowing_land_ids.add(str(row[0]).strip())

        # 2. Fetch Land IDs from active registered sowings (Committed Records)
        if link_internal_record_id:
            res = await session.execute(
                text("SELECT land_id FROM g2p_register_sowings WHERE link_internal_record_id = :rec_id AND record_status = 'ACTIVE'"),
                {"rec_id": link_internal_record_id}
            )
            for row in res.fetchall():
                if row[0] and str(row[0]).strip():
                    sowing_land_ids.add(str(row[0]).strip())

        # 3. Validate current infestation Land ID against the collected Sowing Land IDs
        if str(land_id).strip() not in sowing_land_ids:
            validation_error(f"Land ID '{land_id}' in Pest/Disease Infestation does not match any Land ID specified in Sowing.")

    def _validate_observation_date(self, record: dict) -> None:
        observation_date = parse_date(record.get("observation_date"))
        if observation_date is not None and observation_date > date.today():
            validation_error("observation_date must not be in the future")

    def _validate_estimated_damage(self, record: dict) -> None:
        damage_pct = as_float(record.get("estimated_damage_pct"))
        if damage_pct is not None and not 0 <= damage_pct <= 100:
            validation_error("estimated_damage_pct must be between 0 and 100")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for infestation")

        keys = [
            "functional_record_id",
            "land_id",
            "commodity",
            "growth_stage",
            "infestation_type",
            "pest_name",
            "weed_name",
            "disease_name",
            "chemical_used",
            "severity_level",
            "observation_date",
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
        _logger.info("Constructing record name for infestation")

        keys = ["infestation_type", "severity_level", "observation_date"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
