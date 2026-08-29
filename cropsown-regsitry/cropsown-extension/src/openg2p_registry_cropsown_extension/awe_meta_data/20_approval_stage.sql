INSERT INTO "public"."approval_stage" (
    "id",
    "policy_id",
    "stage_order",
    "name",
    "mode",
    "mode_value",
    "sla_hours",
    "parallel_group",
    "skip_if",
    "on_empty",
    "on_breach",
    "escalation_rules_json",
    "created_at",
    "updated_at"
) VALUES
    ('c3e5071a-3d4f-4081-acb2-3e4f5a6b7c83', 'a1c3e5f7-1b2d-4e6f-8a90-1c2d3e4f5a61', 1, 'Stage 1 Registry Admin', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('e507293c-5f61-42a3-ced4-5a6b7c8d9ea5', 'b2d4f608-2c3e-4f70-9ba1-2d3e4f5a6b72', 1, 'Stage 1 Registry Admin', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW())
ON CONFLICT ("id") DO NOTHING;
