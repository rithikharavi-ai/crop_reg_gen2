import json
import subprocess
import re

# 1. Fetch current schema from Postgres
p_fetch = subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres",
    "psql", "-U", "postgres", "-d", "cropsown", "-t", "-c", 
    "SELECT section_ui_schema FROM g2p_register_sections WHERE section_id = 'cropsown_cultivation_details_section_01';"
], capture_output=True, text=True)

schema_str = p_fetch.stdout.strip()
if not schema_str:
    print("Schema not found!")
    exit(1)

data = json.loads(schema_str)

# 2. Modify the columns
columns = data['panels'][0]['panels'][0]['widgets'][0]['widget-data-columns']

for col in columns:
    if col['column-key'] == 'land_prep_method':
        col['widget-data-source'] = {
            "type": "api",
            "method": "POST",
            "params": {
                "attribute_id": "LAND_PREP_METHOD",
                "page_size": 200
            },
            "service": "attributes",
            "endpoint": "values",
            "labelKey": "value_display",
            "valueKey": "value_id"
        }
    elif col['column-key'] == 'cultivation_type':
        col['widget-data-source'] = {
            "type": "api",
            "method": "POST",
            "params": {
                "attribute_id": "MACHINERY",
                "page_size": 200
            },
            "service": "attributes",
            "endpoint": "values",
            "labelKey": "value_display",
            "valueKey": "value_id"
        }

data['panels'][0]['panels'][0]['widgets'][0]['widget-data-columns'] = columns

# Update DB
json_str = json.dumps(data)
json_str_escaped = json_str.replace("'", "''")

sql = f"UPDATE g2p_register_sections SET section_ui_schema = '{json_str_escaped}' WHERE section_id = 'cropsown_cultivation_details_section_01';"

p_update = subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres",
    "psql", "-U", "postgres", "-d", "cropsown", "-c", sql
], capture_output=True, text=True)

print(p_update.stdout, p_update.stderr)

# Update SQL file
sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"
with open(sql_file, 'r') as f:
    content = f.read()

pattern = rf"\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cultivation_details_section_01','c9ee1d48-93b5-52d5-a8fc-280266a39c10','FALSE','[^']+','[^']+','FALSE',0,'TRUE',10,'(\{{.*?\}})'"
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content[:match.start(1)] + json_str + content[match.end(1):]
    with open(sql_file, 'w') as f:
        f.write(content)
    print("Updated local file too!")
else:
    print("Regex match failed for local file")

