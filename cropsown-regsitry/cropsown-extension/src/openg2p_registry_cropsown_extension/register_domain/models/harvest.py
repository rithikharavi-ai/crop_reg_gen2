"""Harvest lines — a child of CROP_SOWN_RECORDS.

The ERD links every crop line straight to the crop sown record, so this register
sits directly under CropSown with no intermediate land/sowing level; the plot it
applies to is named by `land_uuid` (the stable generated key, not shown in
the UI) and carries the operator-facing `land_id` alongside it.
"""

from datetime import date

from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory
from sqlalchemy import Boolean, Date, Integer, Numeric, String, select
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceHarvest
from .enums import CropMaturityStatusEnum


class G2PHarvest:

    land_uuid: Mapped[str] = mapped_column(String, nullable=True)
    # ── Plot: each line records the land it was worked on (Gen1 puts
    # land_info_id and its attributes on the line, not the header) ───────────
    land_id: Mapped[str] = mapped_column(String, nullable=True)
    is_land_registered: Mapped[bool] = mapped_column(Boolean, nullable=True)
    ownership_type: Mapped[str] = mapped_column(String, nullable=True)        # Attribute lookup (OWNERSHIP_TYPE)
    soil_fertility_type: Mapped[str] = mapped_column(String, nullable=True)   # Attribute lookup (SOIL_FERTILITY)
    plot_category: Mapped[str] = mapped_column(String, nullable=True)         # Attribute lookup (PLOT_CATEGORY)
    land_area: Mapped[float] = mapped_column(Numeric, nullable=True)
    unit: Mapped[str] = mapped_column(String, nullable=True)                  # LandSizeUnitEnum
    sub_kebele: Mapped[str] = mapped_column(String, nullable=True)
    commodity: Mapped[str] = mapped_column(String, nullable=True)             # Attribute lookup (CROP_COMMODITY)
    crop_maturity_status: Mapped[CropMaturityStatusEnum] = mapped_column(String, nullable=True) # CropMaturityStatusEnum
    harvest_date: Mapped[str] = mapped_column(Date, nullable=True)
    area_harvested: Mapped[float] = mapped_column(Numeric, nullable=True)
    qty_harvested: Mapped[float] = mapped_column(Numeric, nullable=True)
    post_harvest_loss_pct: Mapped[float] = mapped_column(Numeric, nullable=True)
    qty_stored: Mapped[float] = mapped_column(Numeric, nullable=True)
    qty_sold: Mapped[float] = mapped_column(Numeric, nullable=True)
    yield_per_ha: Mapped[float] = mapped_column(Numeric, nullable=True)
    harvested_by: Mapped[str] = mapped_column(String, nullable=True)          # Attribute lookup (MACHINERY)

    is_plot_not_registered: Mapped[bool] = mapped_column(Boolean, nullable=True)
    temporary_land_id: Mapped[str] = mapped_column(String, nullable=True)
    sync_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    harvest_date_ec: Mapped[str] = mapped_column(String, nullable=True)
    da_name: Mapped[str] = mapped_column(String, nullable=True)
    da_mobile_number: Mapped[str] = mapped_column(String, nullable=True)
    supervisor_name: Mapped[str] = mapped_column(String, nullable=True)
    supervisor_mobile_number: Mapped[str] = mapped_column(String, nullable=True)



# All Register classes should have the prefix G2PRegister
class G2PRegisterHarvest(G2PRegister, G2PHarvest):
    __tablename__ = "g2p_register_harvests"
    __table_args__ = {"extend_existing": True}

    def get_search_text_fields(self) -> str:
        """Return harvest fields used to build search_text."""
        return G2PRegisterDomainServiceHarvest().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        """Return harvest record_name from domain service implementation."""
        return G2PRegisterDomainServiceHarvest().construct_record_name(self.to_dict())


# All Register History classes should have the prefix G2PRegisterHistory
class G2PRegisterHistoryHarvest(G2PRegisterHistory, G2PHarvest):
    __tablename__ = "g2p_register_history_harvests"
    __table_args__ = {"extend_existing": True}


# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormHarvest(G2PIntakeForm, G2PRegister, G2PHarvest):
    __tablename__ = "g2p_intake_form_harvests"
    __table_args__ = {"extend_existing": True}

    async def get_link_internal_record_id(self, session):
        from .crop_sown import G2PIntakeFormCropSown
        result = await session.execute(
            select(G2PIntakeFormCropSown).where(
                G2PIntakeFormCropSown.submission_id == self.submission_id
            )
        )
        crop_sown = result.scalars().first()
        if crop_sown:
            self.link_internal_record_id = crop_sown.internal_record_id

    def get_search_text_fields(self) -> str:
        """Return harvest fields used to build search_text."""
        return G2PRegisterDomainServiceHarvest().construct_search_text(self.to_dict())

    def get_record_name_fields(self) -> str:
        """Return harvest record_name from domain service implementation."""
        return G2PRegisterDomainServiceHarvest().construct_record_name(self.to_dict())
