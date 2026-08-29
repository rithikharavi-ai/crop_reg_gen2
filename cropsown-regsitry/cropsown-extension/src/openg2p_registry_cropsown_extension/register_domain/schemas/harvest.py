from datetime import date
from typing import Optional

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)
from ..models.enums import CropMaturityStatusEnum


class G2PSchemaHarvest:

    is_plot_not_registered: Optional[bool] = None
    temporary_land_id: Optional[str] = None
    sync_id: Optional[str] = None
    harvest_date_ec: Optional[str] = None
    land_uuid: Optional[str] = None
    land_id: Optional[str] = None
    is_land_registered: Optional[bool] = None
    ownership_type: Optional[str] = None
    soil_fertility_type: Optional[str] = None
    plot_category: Optional[str] = None
    land_area: Optional[float] = None
    unit: Optional[str] = None
    sub_kebele: Optional[str] = None
    commodity: Optional[str] = None
    crop_maturity_status: Optional[CropMaturityStatusEnum] = None
    harvest_date: Optional[date] = None
    area_harvested: Optional[float] = None
    qty_harvested: Optional[float] = None
    post_harvest_loss_pct: Optional[float] = None
    qty_stored: Optional[float] = None
    qty_sold: Optional[float] = None
    yield_per_ha: Optional[float] = None
    harvested_by: Optional[str] = None
    da_name: Optional[str] = None
    da_mobile_number: Optional[str] = None
    supervisor_name: Optional[str] = None
    supervisor_mobile_number: Optional[str] = None



class G2PRegisterSchemaHarvest(G2PRegisterBaseSchema, G2PSchemaHarvest):
    """
    Schema for Harvest register.
    Inherits fields from G2PRegisterBaseSchema.
    Attributes inherited from G2PSchemaHarvest are specific to the Harvest domain.
    """


class G2PRegisterHistorySchemaHarvest(G2PRegisterHistorySchema, G2PSchemaHarvest):
    """
    Schema for Harvest history.
    Inherits fields from G2PRegisterHistorySchema.
    """


class G2PIntakeFormSchemaHarvest(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaHarvest):
    """
    Schema for Harvest intake form.
    Inherits fields from G2PRegisterBaseSchema.
    Attributes inherited from G2PSchemaHarvest are specific to the Harvest domain and are included in the intake form schema for data collection.
    """
