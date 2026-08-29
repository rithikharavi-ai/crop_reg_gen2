import json
import subprocess

# 1. Fetch cropsown_cluster_details_section_01
res = subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres", "psql", "-U", "postgres", "-d", "cropsown", "-t", "-c",
    "SELECT section_ui_schema FROM g2p_register_sections WHERE section_id = 'cropsown_cluster_details_section_01';"
], capture_output=True, text=True)

schema_str = res.stdout.strip()
if not schema_str:
    print("Schema not found!")
    exit(1)

data = json.loads(schema_str)

# Update fields
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

# Also add them to visible columns if desired
visible = data['panels'][0]['panels'][0]['widgets'][0].get('widget-data-visible-columns', [])
# let's leave visible columns mostly as is or adjust them if needed.

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
    section_uuid, section_id, section_ui_schema_id, is_multiple_record,
    record_path, label, display_title, weight, visible, section_ui_schema,
    is_deleted, is_custom, created_by, updated_by
) VALUES (
    gen_random_uuid(), 'cropsown_cultivation_cluster_details_section_01',
    gen_random_uuid(), FALSE, 'cs_cultivation_cluster_details',
    'Cultivation Cluster Information Details', FALSE, 0, TRUE,
    '{json_str}', FALSE, FALSE, 'system', 'system'
) ON CONFLICT (section_id) DO UPDATE SET section_ui_schema = '{json_str}';
"""

# Insert into UI Tabs
sql += """
INSERT INTO g2p_register_ui_tab_sections (tab_section_id, tab_id, section_id, section_order)
VALUES (gen_random_uuid(), 'cropsown_cultivation_tab', 'cropsown_cultivation_cluster_details_section_01', 20)
ON CONFLICT DO NOTHING;

INSERT INTO g2p_intake_form_ui_tab_sections (tab_section_id, tab_id, section_id, section_order)
VALUES (gen_random_uuid(), 'f3f3a330-98f4-5941-9cec-303e77462b14', 'cropsown_cultivation_cluster_details_section_01', 40)
ON CONFLICT DO NOTHING;
"""

with open('insert_cultivation_cluster.sql', 'w') as f:
    f.write(sql)

subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres", "psql", "-U", "postgres", "-d", "cropsown", "-f", "-"
], stdin=open('insert_cultivation_cluster.sql'))
print("DB updated")

