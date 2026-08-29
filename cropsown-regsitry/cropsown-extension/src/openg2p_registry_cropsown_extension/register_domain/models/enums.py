"""Enumerations for values the ERD does NOT model as lookup tables.

Everything the "CROP SOWN REGISTRY ERD UPDATED" draws as a catalog or lookup
table (crop, crop variety, season, plot category, ownership type, soil
fertility, fertilizer type, land preparation method, water source, infestation
type, cluster status, approval/workflow status) is an **attribute lookup**
instead — a plain String column resolved against g2p_attributes /
g2p_attribute_values, so the values are data an administrator can extend rather
than code. What remains here are the closed value sets the ERD leaves as plain
columns.
"""

from enum import StrEnum


class LandSizeUnitEnum(StrEnum):
    HECTARE = "HECTARE"
    TIMAD = "TIMAD"
    ACRE = "ACRE"
    SQUARE_METER = "SQUARE_METER"


class CroppingSystemEnum(StrEnum):
    MONO_CROPPING = "MONO_CROPPING"
    INTER_CROPPING = "INTER_CROPPING"
    MIXED_CROPPING = "MIXED_CROPPING"
    RELAY_CROPPING = "RELAY_CROPPING"


class SeedClassEnum(StrEnum):
    LOCAL = "LOCAL"
    IMPROVED = "IMPROVED"


class SeedSourceEnum(StrEnum):
    OWN_SAVED = "OWN_SAVED"
    COOPERATIVE = "COOPERATIVE"
    GOVERNMENT = "GOVERNMENT"
    MARKET = "MARKET"
    NGO = "NGO"


class SowingStatusEnum(StrEnum):
    NOT_SOWN = "NOT_SOWN"
    PARTIALLY_SOWN = "PARTIALLY_SOWN"
    FULLY_SOWN = "FULLY_SOWN"
    RE_SOWN = "RE_SOWN"


class CropMaturityStatusEnum(StrEnum):
    IMMATURE = "IMMATURE"
    MATURING = "MATURING"
    READY_FOR_HARVEST = "READY_FOR_HARVEST"
    HARVESTED = "HARVESTED"


class GrowthStageEnum(StrEnum):
    EMERGENCE = "EMERGENCE"
    VEGETATIVE = "VEGETATIVE"
    FLOWERING = "FLOWERING"
    MATURITY = "MATURITY"


class SeverityLevelEnum(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AgroEcologicalZoneEnum(StrEnum):
    KOLLA = "KOLLA"
    WOINA_DEGA = "WOINA_DEGA"
    DEGA = "DEGA"
    WURCH = "WURCH"
    BEREHA = "BEREHA"


class LifecycleStageEnum(StrEnum):
    """The Odoo lifecycle ladder, in order."""
    DRAFT = "DRAFT"
    PENDING_PLANNING = "PENDING_PLANNING"
    PLANNING_REJECTED = "PLANNING_REJECTED"
    PLANNING_APPROVED = "PLANNING_APPROVED"
    PENDING_CULTIVATION = "PENDING_CULTIVATION"
    CULTIVATION_REJECTED = "CULTIVATION_REJECTED"
    CULTIVATION_APPROVED = "CULTIVATION_APPROVED"
    PENDING_SOWING = "PENDING_SOWING"
    SOWING_REJECTED = "SOWING_REJECTED"
    SOWING_APPROVED = "SOWING_APPROVED"
    PENDING_HARVESTING = "PENDING_HARVESTING"
    HARVESTING_REJECTED = "HARVESTING_REJECTED"
    HARVESTING_APPROVED = "HARVESTING_APPROVED"


class StageStateEnum(StrEnum):
    """Per-stage approval state (Odoo: planning_state / cultivation_state /
    sowing_state / harvesting_state)."""
    DRAFT = "DRAFT"
    PENDING_WAH = "PENDING_WAH"
    REJECTED = "REJECTED"
    UPDATE_REQUESTED = "UPDATE_REQUESTED"
    APPROVED = "APPROVED"


class RejectedAtStageEnum(StrEnum):
    SMS = "SMS"
    WAH = "WAH"


class EditStateEnum(StrEnum):
    OPEN = "OPEN"
    LOCKED = "LOCKED"
