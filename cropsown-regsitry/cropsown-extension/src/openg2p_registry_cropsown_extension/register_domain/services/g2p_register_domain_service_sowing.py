import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_validation_utils import as_float, parse_date, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceSowing(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_sowing_date(record)
            self._validate_area_sown(record)
            self._validate_seed_quantity(record)

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
            "land_uuid",
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
