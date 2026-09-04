import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_compute_utils import (
    compute_fertilizer_sacks,
    compute_season_parts,
    is_date_in_season,
    compute_ec_date
)

from .domain_validation_utils import as_float, parse_date, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceCultivation(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict], **kwargs):
        for record in records:

            from .domain_validation_utils import validate_alphabetical_name, validate_mobile_number
            validate_alphabetical_name(record.get("farmer_name"), "Farmer Name")
            validate_alphabetical_name(record.get("da_name"), "DA Name")
            validate_alphabetical_name(record.get("supervisor_name"), "Supervisor Name")
            validate_mobile_number(record.get("da_mobile_number"), "DA Mobile Number")
            validate_mobile_number(record.get("supervisor_mobile_number"), "Supervisor Mobile Number")
            compute_season_parts(record)
            compute_fertilizer_sacks(record, "actual_fertilizer_qty", "actual_fertilizer_sack")
            self._validate_date_in_season(record, "actual_planted_date")
            self._validate_actual_planted_date(record)
            self._validate_actual_crop_area(record)
            compute_ec_date(record, "actual_planted_date", "actual_planted_date_ec")

    def _validate_actual_planted_date(self, record: dict) -> None:
        planted_date = parse_date(record.get("actual_planted_date"))
        if planted_date is not None and planted_date > date.today():
            validation_error("actual_planted_date must not be in the future")

    def _validate_actual_crop_area(self, record: dict) -> None:
        crop_area = as_float(record.get("actual_crop_area"))
        if crop_area is not None and crop_area <= 0:
            validation_error("actual_crop_area must be greater than zero when provided")
            
        land_area = as_float(record.get("land_area"))
        if crop_area is not None and land_area is not None:
            if crop_area > land_area:
                validation_error(f"Actual Crop Area ({crop_area} ha) cannot be greater than Total Land Area ({land_area} ha).")

    def _validate_date_in_season(self, record: dict, field: str) -> None:
        """Odoo: `_check_season_crop_required` — the date must fall inside the
        season window carried on the record."""
        value = parse_date(record.get(field))
        if value is None:
            return
        if not is_date_in_season(value, record.get("start_month"), record.get("start_day"),
                                 record.get("end_month"), record.get("end_day")):
            validation_error(f"{field} falls outside the season window on this record")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for cultivation")

        keys = [
            "functional_record_id",
            "land_id",
            "season",
            "commodity",
            "crop_variety",
            "crop_category",
            "land_prep_method",
            "cultivation_type",
            "cropping_system",
            "actual_crop_area",
            "actual_seed_class",
            "actual_seed_source",
            "actual_fertilizer_type",
            "water_source",
            "water_source_method",
            "water_source_frequency",
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
        _logger.info("Constructing record name for cultivation")

        keys = ["commodity", "land_prep_method", "actual_crop_area"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
