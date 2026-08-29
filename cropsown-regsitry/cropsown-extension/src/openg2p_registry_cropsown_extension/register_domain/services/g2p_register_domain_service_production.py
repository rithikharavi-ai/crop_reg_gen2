import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_compute_utils import compute_production_results

from .domain_validation_utils import as_float, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceProduction(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            compute_production_results(record)
            self._validate_area_under_production(record)
            self._validate_yields(record)

    def _validate_area_under_production(self, record: dict) -> None:
        area = as_float(record.get("area_under_production"))
        if area is not None and area <= 0:
            validation_error("area_under_production must be greater than zero when provided")

    def _validate_yields(self, record: dict) -> None:
        for field in ("expected_yield", "actual_yield", "yield_per_ha"):
            value = as_float(record.get(field))
            if value is not None and value < 0:
                validation_error(f"{field} must not be negative")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for production")

        keys = [
            "functional_record_id",
            "land_uuid",
            "land_id",
            "season",
            "commodity",
            "crop_variety",
            "crop_category",
            "growth_stage",
            "area_under_production",
            "expected_yield",
            "actual_yield",
            "water_source",
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
        _logger.info("Constructing record name for production")

        keys = ["commodity", "season", "actual_yield"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
