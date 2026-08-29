INSERT INTO g2p_register_definitions (
    register_id, register_mnemonic, register_subject, register_description,
    master_register_id, register_rank, functional_id_generation_required,
    register_purpose, has_image, dedup_is_enabled, completion_score_required,
    outgest_applicable, requires_registrant_authentication,
    registrant_authentication_validity_days, registrant_re_auth_warning_days_before
) VALUES (
    '3392fa94-39fa-5eb7-891d-e593ab973e21', 'CultivationCluster', 'Cultivation Cluster Info',
    'Cultivation Cluster Information Register', '6b06a95a-9a6c-5a33-a33d-c1625716c59c',
    80, FALSE, 'TABLE', FALSE, FALSE, FALSE, FALSE, FALSE, 730, 30
);
