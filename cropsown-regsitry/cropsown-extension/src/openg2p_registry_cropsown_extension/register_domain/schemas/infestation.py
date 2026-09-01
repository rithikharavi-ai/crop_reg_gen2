from datetime import date
from typing import Optional, List

from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)
from ..models.enums import GrowthStageEnum, SeverityLevelEnum


class G2PSchemaInfestation:

    infestation_id: Optional[str] = None
    is_plot_not_registered: Optional[bool] = None
    temporary_land_id: Optional[str] = None
    sync_id: Optional[str] = None
    observation_date_ec: Optional[str] = None
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
    growth_stage: Optional[GrowthStageEnum] = None
    cluster_status: Optional[List[str]] = None
    infestation_type: Optional[List[str]] = None
    pest_name: Optional[str] = None
    weed_name: Optional[str] = None
    disease_name: Optional[str] = None
    chemical_used: Optional[str] = None
    severity_level: Optional[SeverityLevelEnum] = None
    estimated_damage_pct: Optional[float] = None
    observation_date: Optional[date] = None
    geo_tagged_photo_document_id: Optional[str] = None
    action_taken: Optional[str] = None


class G2PRegisterSchemaInfestation(G2PRegisterBaseSchema, G2PSchemaInfestation):
    """
    Schema for Infestation Incident register.
    Inherits fields from G2PRegisterBaseSchema.
    Attributes inherited from G2PSchemaInfestation are specific to the Infestation Incident domain.
    """


class G2PRegisterHistorySchemaInfestation(G2PRegisterHistorySchema, G2PSchemaInfestation):
    """
    Schema for Infestation Incident history.
    Inherits fields from G2PRegisterHistorySchema.
    """


class G2PIntakeFormSchemaInfestation(G2PIntakeFormSchemaBase, G2PRegisterBaseSchema, G2PSchemaInfestation):
    """
    Schema for Infestation Incident intake form.
    Inherits fields from G2PRegisterBaseSchema.
    Attributes inherited from G2PSchemaInfestation are specific to the Infestation Incident domain and are included in the intake form schema for data collection.
    """
