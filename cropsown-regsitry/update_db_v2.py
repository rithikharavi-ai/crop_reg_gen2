import json
import subprocess

res = subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres", "psql", "-U", "postgres", "-d", "cropsown", "-t", "-c",
    "SELECT section_ui_schema FROM g2p_register_sections WHERE section_id = 'cropsown_cluster_details_section_01';"
], capture_output=True, text=True)

schema_str = res.stdout.strip()
if not schema_str:
    print("Schema not found!")
    exit(1)

data = json.loads(schema_str)

columns = data['panels'][0]['panels'][0]['widgets'][0]['widget-data-columns']
for col in columns:
    if col['column-key'] == 'cluster_plan':
        col['widget-label'] = 'Actual Plan (ha)'
    elif col['column-key'] == 'collected_land':
        col['widget-label'] = 'Actual Collected Land (Quintal)'
    elif col['column-key'] == 'collected_quintal':
        col['widget-label'] = 'Actual Collected Quintal'
    elif col['column-key'] == 'collected_by_combiner':
        col['widget-label'] = 'Actual Collected by Combiner (ha)'

data['panels'][0]['panels'][0]['widgets'][0]['widget-data-dialog-title-add'] = 'Add Cultivation Cluster'
data['panels'][0]['panels'][0]['widgets'][0]['widget-data-dialog-title-edit'] = 'Edit Cultivation Cluster'
data['panels'][0]['panels'][0]['widgets'][0]['widget-label'] = 'Cultivation Cluster Information'
data['section-id'] = 'cropsown_cultivation_cluster_details_section_01'
data['section-title'] = 'Cultivation Cluster Information Details'
data['panels'][0]['panels'][0]['widgets'][0]['widget-id'] = 'cs_cultivation_cluster_details_table'
data['panels'][0]['panels'][0]['widgets'][0]['widget-data-path'] = 'new-uuid-placeholder.records'

json_str = json.dumps(data).replace("'", "''")

sql = f"""
INSERT INTO g2p_register_sections (
    register_id, section_id, section_register_id, is_core_section,
    section_mnemonic, documents_required, no_of_verifications_required,
    is_list, section_weightage, section_ui_schema, cr_auto_approve_for_bene_portal,
    cr_auto_approve_for_agent_portal, cr_auto_approve_for_staff_portal, cr_auto_approve_for_partner
) VALUES (
    'cropsown', 'cropsown_cultivation_cluster_details_section_01',
    '3392fa94-39fa-5eb7-891d-e593ab973e21', FALSE, 'cs_cultivation_cluster_details',
    FALSE, 0, TRUE, 10, '{json_str}', FALSE, FALSE, FALSE, FALSE
) ON CONFLICT (section_id) DO UPDATE SET section_ui_schema = '{json_str}';

INSERT INTO g2p_register_ui_tab_sections (tab_section_id, register_id, tab_id, section_id, section_order)
VALUES (gen_random_uuid(), 'cropsown', 'cropsown_cultivation_tab', 'cropsown_cultivation_cluster_details_section_01', 20)
ON CONFLICT DO NOTHING;

INSERT INTO g2p_intake_form_ui_tab_sections (tab_section_id, tab_id, section_id, section_order)
VALUES (gen_random_uuid(), 'f3f3a330-98f4-5941-9cec-303e77462b14', 'cropsown_cultivation_cluster_details_section_01', 40)
ON CONFLICT DO NOTHING;
"""

with open('insert_cultivation_cluster_v2.sql', 'w') as f:
    f.write(sql)

subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres", "psql", "-U", "postgres", "-d", "cropsown", "-f", "-"
], stdin=open('insert_cultivation_cluster_v2.sql'))
print("DB updated")

