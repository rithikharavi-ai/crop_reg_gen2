INSERT INTO "public"."g2p_registry_awe_policy_configurations" (
    "awe_policy_config_id",
    "policy_scope",
    "register_id",
    "intake_form_id",
    "section_id",
    "policy_type",
    "policy_key",
    "context_field_names"
) VALUES
    ('7c1f8a92-4b3d-4e15-9a26-5d8e0f3b71a4', 'REGISTER', '6b06a95a-9a6c-5a33-a33d-c1625716c59c', '', '', 'registry.change_request', 'registry.change_request.cropsown', 'null'),
    ('8d2e9ba3-5c4e-4f26-ab37-6e9f1a4c82b5', 'INTAKE_FORM', '6b06a95a-9a6c-5a33-a33d-c1625716c59c', '852cf76a-a691-5572-9dd2-9bbca6fa5c78', '', 'registry.intake_form', 'registry.intake_form.cropsown', 'null')
ON CONFLICT ("awe_policy_config_id") DO NOTHING;
