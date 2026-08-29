INSERT INTO g2p_register_sections (
    section_id, section_ui_schema_id, is_multiple_record,
    record_path, label, display_title, weight, visible, section_ui_schema,
    is_deleted, is_custom
)
SELECT
    'cropsown_cultivation_cluster_details_section_01',
    gen_random_uuid(), FALSE, 'cs_cultivation_cluster_details',
    'Cultivation Cluster Information Details', FALSE, 0, TRUE,
    section_ui_schema, FALSE, FALSE
FROM g2p_register_sections WHERE section_id = 'cropsown_cluster_details_section_01'
ON CONFLICT DO NOTHING;

-- Now update the schema for the newly inserted row to reflect the label changes
-- I'll use Python for this part again because modifying JSON in PostgreSQL directly is complex.
