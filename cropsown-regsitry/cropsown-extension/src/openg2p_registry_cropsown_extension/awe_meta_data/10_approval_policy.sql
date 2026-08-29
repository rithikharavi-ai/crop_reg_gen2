INSERT INTO "public"."approval_policy" (
    "id",
    "policy_key",
    "version",
    "name",
    "description",
    "status",
    "artifact_type",
    "created_by",
    "forbid_self_approval",
    "forbid_repeat_approvers",
    "created_at",
    "updated_at"
) VALUES
    ('a1c3e5f7-1b2d-4e6f-8a90-1c2d3e4f5a61', 'registry.change_request.cropsown', 1, 'Policy for Crop Sown Change Request', NULL, 'active', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('b2d4f608-2c3e-4f70-9ba1-2d3e4f5a6b72', 'registry.intake_form.cropsown', 1, 'Policy for Crop Sown Intake Form', NULL, 'active', 'registry.intake_form', 'seed', 'FALSE', 'FALSE', NOW(), NOW())
ON CONFLICT ("id") DO NOTHING;
