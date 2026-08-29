INSERT INTO "public"."approver_rule" (
    "id",
    "stage_id",
    "rule_type",
    "rule_value",
    "kind",
    "required",
    "created_at",
    "updated_at"
) VALUES
    ('0a1b2c3d-7183-44c5-8ff6-7c8d9eafb0c7', 'c3e5071a-3d4f-4081-acb2-3e4f5a6b7c83', 'user', '{"user_id": "admin"}', 'approver', 'FALSE', NOW(), NOW()),
    ('2c3d4e5f-93a5-46e7-a1b8-9eafb0c1d2e9', 'e507293c-5f61-42a3-ced4-5a6b7c8d9ea5', 'user', '{"user_id": "admin"}', 'approver', 'FALSE', NOW(), NOW())
ON CONFLICT ("id") DO NOTHING;
