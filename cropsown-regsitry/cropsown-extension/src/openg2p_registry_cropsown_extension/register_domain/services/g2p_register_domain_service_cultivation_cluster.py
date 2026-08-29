import logging

from openg2p_registry_core.services import G2PRegisterDomainService

from .domain_compute_utils import compute_cluster_area, compute_season_parts

from .domain_validation_utils import as_float, as_int, validation_error

_logger = logging.getLogger("g2p-register-domain-service")


class G2PRegisterDomainServiceCultivationCluster(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            compute_season_parts(record)
            compute_cluster_area(record)
            self._validate_cluster_area(record)
            self._validate_smallholders(record)
            self._validate_collected_land(record)

    def _validate_cluster_area(self, record: dict) -> None:
        area = as_float(record.get("cluster_area_hectare"))
        if area is not None and area <= 0:
            validation_error("cluster_area_hectare must be greater than zero when provided")

    def _validate_smallholders(self, record: dict) -> None:
        for field in ("number_of_smallholders",):
            value = as_int(record.get(field))
            if value is not None and value < 0:
                validation_error(f"{field} must not be negative")

    def _validate_collected_land(self, record: dict) -> None:
        area = as_float(record.get("cluster_area_hectare"))
        collected = as_float(record.get("collected_land"))
        if area is not None and collected is not None and collected > area:
            validation_error("collected_land must not exceed cluster_area_hectare")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for cluster")

        keys = [
            "functional_record_id",
            "cluster_name",
            "agro_ecological_zone",
            "season",
            "cluster_area_hectare",
            "water_source",
            "water_source_method",
            "water_source_frequency",
            "latitude",
            "longitude",
            "region",
            "zone",
            "woreda",
            "kebele",
            "sub_kebele",
            "address_line_1",
            "address_line_2",
            "country_code",
            "da_name",
            "da_mobile_number",
            "supervisor_name",
            "supervisor_mobile_number",
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
        _logger.info("Constructing record name for cluster")

        keys = ["cluster_name", "season"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
