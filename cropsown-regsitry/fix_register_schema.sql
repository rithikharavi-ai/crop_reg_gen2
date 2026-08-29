INSERT INTO g2p_register_schemas (
    register_id, deduplicate_schema, search_result_schema, filter_schema
)
SELECT
    '3392fa94-39fa-5eb7-891d-e593ab973e21', deduplicate_schema, search_result_schema, filter_schema
FROM g2p_register_schemas
WHERE register_id = '62098187-a3f7-517a-be6d-b25da981153e'
ON CONFLICT DO NOTHING;
