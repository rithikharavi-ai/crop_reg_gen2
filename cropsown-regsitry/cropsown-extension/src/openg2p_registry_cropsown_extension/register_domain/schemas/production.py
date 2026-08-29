from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)
from ..models.enums import GrowthStageEnum


class G2PSchemaProduction:

    is_plot_not_registered: Optional[bool] = None
    temporary_land_id: Optional[str] = None
    sync_id: Optional[str] = None
    actual_sowing_date: Optional[date] = None
    yield_performance_pct: Optional[float] = None
    geo_tagged_photo_document_id: Optional[str] = None
    land_uuid: Optional[str] = None
    land_id: Optional[str] = None
    is_land_registered: Optional[bool] = None
    ownership_type: Optional[str] = None
    soil_fertility_type: Optional[str] = None
    plot_category: Optional[str] = None
    land_area: Optional[float] = None
    unit: Optional[str] = None
    sub_kebele: Optional[str] = None
    season: Optional[str] = None
    commodity: Optional[str] = None
    crop_variety: Optional[str] = None
    crop_category: Optional[str] = None
    growth_stage: Optional[GrowthStageEnum] = None
    area_under_production: Optional[float] = None
    expected_yield: Optional[float] = None
    actual_yield: Optional[float] = None
    yield_per_ha: Optional[float] = None
    land_utilization_rate: Optional[float] = None
    seed_productivity: Optional[float] = None
    fertilizer_efficiency: Optional[float] = None
    water_source: Optional[str] = None
    remark: Optional[str] = None


class G2PRegisterSchemaProduction(G2PRegisterBaseSchema, G2PSchemaProduction):
    """
    Schema for Crop Production register.
    Inherits fields from G2PRegisterBaseSchema.
    Attributes inherited from G2PSchemaProduction are specific to the Crop Production domain.
    """


class G2PRegisterHistorySchemaProduction(G2PRegisterHistorySchema, G2PSchemaProduction):
    """
    Schema for Crop Production history.
    Inherits fields from G2PRegisterHistorySchema.
    """


class G2PIntakeFormSchemaProduction(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaProduction):
    """
    Schema for Crop Production intake form.
    Inherits fields from G2PRegisterBaseSchema.
    Attributes inherited from G2PSchemaProduction are specific to the Crop Production domain and are included in the intake form schema for data collection.
    """
