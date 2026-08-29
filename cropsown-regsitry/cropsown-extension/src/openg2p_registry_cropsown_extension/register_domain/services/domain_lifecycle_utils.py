"""The crop sown lifecycle, ported from the Odoo registry's approval actions.

Gen1 drives four per-stage states (planning / cultivation / sowing / harvesting)
and one `lifecycle_stage` ladder, advanced by `action_approve_wah`,
`action_reject` and `action_set_draft`. Approving a stage marks it APPROVED,
moves the ladder to that stage's approved rung, and opens the next stage in
DRAFT.

Approval itself is AWE's job here, so this module holds only the transition
table and the helpers that apply it — the domain service calls them from
`post_approve`, once AWE reports a terminal decision.
"""

# The rung and state names are written as plain strings rather than imported
# from ..models.enums: the models package imports this package back (models ->
# services -> here), so importing the enums at module level closes a cycle.
# These mirror LifecycleStageEnum / StageStateEnum / RejectedAtStageEnum exactly;
# tests/test_lifecycle_enums.py asserts the two never drift.


class LifecycleStageEnum:
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


class StageStateEnum:
    DRAFT = "DRAFT"
    PENDING_WAH = "PENDING_WAH"
    REJECTED = "REJECTED"
    UPDATE_REQUESTED = "UPDATE_REQUESTED"
    APPROVED = "APPROVED"


class RejectedAtStageEnum:
    SMS = "SMS"
    WAH = "WAH"

# stage -> (its state field, the rung it reaches when approved,
#           the rung it sits on while pending, its rejected rung, the next stage)
STAGES = {
    "planning": (
        "planning_state",
        LifecycleStageEnum.PLANNING_APPROVED,
        LifecycleStageEnum.PENDING_PLANNING,
        LifecycleStageEnum.PLANNING_REJECTED,
        "cultivation",
    ),
    "cultivation": (
        "cultivation_state",
        LifecycleStageEnum.CULTIVATION_APPROVED,
        LifecycleStageEnum.PENDING_CULTIVATION,
        LifecycleStageEnum.CULTIVATION_REJECTED,
        "sowing",
    ),
    "sowing": (
        "sowing_state",
        LifecycleStageEnum.SOWING_APPROVED,
        LifecycleStageEnum.PENDING_SOWING,
        LifecycleStageEnum.SOWING_REJECTED,
        "harvesting",
    ),
    "harvesting": (
        "harvesting_state",
        LifecycleStageEnum.HARVESTING_APPROVED,
        LifecycleStageEnum.PENDING_HARVESTING,
        LifecycleStageEnum.HARVESTING_REJECTED,
        None,
    ),
}

# Which stage a change to a given section belongs to, so an approval can be
# routed without the caller naming the stage.
SECTION_STAGE = {
    "cs_planning_details": "planning",
    "cs_cultivation_details": "cultivation",
    "cs_sowing_details": "sowing",
    "cs_production_details": "sowing",
    "cs_harvest_details": "harvesting",
    "cs_infestation_details": "sowing",
    "cs_cluster_details": "planning",
}

# The rung a record sits on before anything has been approved.
INITIAL_STAGE = LifecycleStageEnum.DRAFT


def stage_for_section(section_mnemonic: str) -> str | None:
    """Map the edited section back to the lifecycle stage it belongs to."""
    return SECTION_STAGE.get((section_mnemonic or "").strip())


def current_stage(record) -> str:
    """The stage a record is waiting on — the first not yet approved."""
    for stage, (state_field, *_rest) in STAGES.items():
        if getattr(record, state_field, None) != StageStateEnum.APPROVED:
            return stage
    return "harvesting"


def apply_approval(record, stage: str) -> None:
    """Odoo: `action_approve_wah`.

    Marks the stage approved, moves the ladder to its approved rung, and opens
    the next stage in DRAFT. Re-approving an already-approved stage is a no-op
    so a replayed webhook cannot push the ladder forward twice.
    """
    if stage not in STAGES:
        return
    state_field, approved_rung, _pending, _rejected, next_stage = STAGES[stage]
    if getattr(record, state_field, None) == StageStateEnum.APPROVED:
        return

    setattr(record, state_field, StageStateEnum.APPROVED)
    record.lifecycle_stage = approved_rung
    record.rejection_reason = None
    record.rejected_at_stage = None

    if next_stage:
        next_state_field = STAGES[next_stage][0]
        if getattr(record, next_state_field, None) in (None, ""):
            setattr(record, next_state_field, StageStateEnum.DRAFT)


def apply_rejection(record, stage: str, reason: str | None = None,
                    at_stage: str = RejectedAtStageEnum.WAH) -> None:
    """Odoo: `action_reject` — records why, and where in the chain it stopped."""
    if stage not in STAGES:
        return
    state_field, _approved, _pending, rejected_rung, _next = STAGES[stage]
    setattr(record, state_field, StageStateEnum.REJECTED)
    record.lifecycle_stage = rejected_rung
    record.rejection_reason = reason or None
    record.rejected_at_stage = at_stage


def apply_set_draft(record, stage: str) -> None:
    """Odoo: `action_set_draft` — send a stage back for rework."""
    if stage not in STAGES:
        return
    state_field, _approved, _pending, _rejected, _next = STAGES[stage]
    setattr(record, state_field, StageStateEnum.DRAFT)
    record.lifecycle_stage = INITIAL_STAGE if stage == "planning" else record.lifecycle_stage


def mark_pending(record, stage: str) -> None:
    """A submitted stage awaits approval."""
    if stage not in STAGES:
        return
    state_field, _approved, pending_rung, _rejected, _next = STAGES[stage]
    setattr(record, state_field, StageStateEnum.PENDING_WAH)
    record.lifecycle_stage = pending_rung
