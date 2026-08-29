import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_compute_utils import compute_harvest_yield

from .domain_validation_utils import as_float, parse_date, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceHarvest(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            compute_harvest_yield(record)
            self._validate_harvest_date(record)
            self._validate_post_harvest_loss(record)
            self._validate_disposal_quantities(record)

    def _validate_harvest_date(self, record: dict) -> None:
        harvest_date = parse_date(record.get("harvest_date"))
        if harvest_date is not None and harvest_date > date.today():
            validation_error("harvest_date must not be in the future")

    def _validate_post_harvest_loss(self, record: dict) -> None:
        loss_pct = as_float(record.get("post_harvest_loss_pct"))
        if loss_pct is not None and not 0 <= loss_pct <= 100:
            validation_error("post_harvest_loss_pct must be between 0 and 100")

    def _validate_disposal_quantities(self, record: dict) -> None:
        qty_harvested = as_float(record.get("qty_harvested"))
        if qty_harvested is None:
            return
        disposed = sum(
            value
            for value in (
                as_float(record.get("qty_stored")),
                as_float(record.get("qty_sold")),
            )
            if value is not None
        )
        if disposed > qty_harvested:
            validation_error(
                "qty_stored and qty_sold together must not exceed qty_harvested"
            )

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for harvest")

        keys = [
            "functional_record_id",
            "land_uuid",
            "land_id",
            "commodity",
            "crop_maturity_status",
            "harvest_date",
            "area_harvested",
            "qty_harvested",
            "qty_stored",
            "qty_sold",
            "harvested_by",
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
        _logger.info("Constructing record name for harvest")

        keys = ["commodity", "harvest_date", "qty_harvested"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
