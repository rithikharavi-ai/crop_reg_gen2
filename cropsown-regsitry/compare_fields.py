import json
import re

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

pattern = re.compile(r"(\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cluster_details_section_01'.*?'({.*?}?)','FALSE','FALSE','FALSE','FALSE'\))")
match = pattern.search(content)
if not match:
    print("Could not find schema")
    exit(1)

schema_str = match.group(2)
# Need to unescape the JSON if it's double-quoted, wait, it's just raw string in SQL
import ast
schema = json.loads(schema_str)

columns = []
for panel in schema.get('panels', []):
    for subpanel in panel.get('panels', []):
        for widget in subpanel.get('widgets', []):
            if widget.get('widget') == 'dialog-table':
                for col in widget.get('widget-data-columns', []):
                    columns.append(col.get('column-key'))

print("UI columns:", columns)

# Now read cluster.py
cluster_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/register_domain/models/cluster.py"
with open(cluster_file, 'r') as f:
    cluster_py = f.read()

model_fields = re.findall(r"    ([a-zA-Z0-9_]+): Mapped\[", cluster_py)
print("\nModel fields:", model_fields)

print("\nFields in Model but NOT in UI:", set(model_fields) - set(columns))
print("Fields in UI but NOT in Model:", set(columns) - set(model_fields))
