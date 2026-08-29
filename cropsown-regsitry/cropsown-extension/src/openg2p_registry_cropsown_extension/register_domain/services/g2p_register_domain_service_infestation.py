import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import as_float, parse_date, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceInfestation(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_observation_date(record)
            self._validate_estimated_damage(record)

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
            "land_uuid",
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
