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

columns = data['panels'][0]['panels'][0]['widgets'][0]['widget-data-columns']

# Check if season is missing
if not any(c['column-key'] == 'season' for c in columns):
    season_col = {
        "widget": "select",
        "column-key": "season",
        "widget-type": "input",
        "widget-label": "Season",
        "widget-readonly": False,
        "widget-data-path": "season",
        "widget-data-source": {
            "type": "api",
            "method": "POST",
            "params": {
                "attribute_id": "CROP_SEASON",
                "page_size": 200
            },
            "service": "attributes",
            "endpoint": "values",
            "labelKey": "value_display",
            "valueKey": "value_id"
        }
    }
    # Insert it right before commodity
    idx = next((i for i, c in enumerate(columns) if c['column-key'] == 'commodity'), 0)
    columns.insert(idx, season_col)

# Let's ensure remark is visible if they mean the data table
visible_columns = data['panels'][0]['panels'][0]['widgets'][0].get('widget-data-visible-columns', [])
if 'remark' not in visible_columns:
    visible_columns.append('remark')
if 'season' not in visible_columns:
    visible_columns.append('season')
data['panels'][0]['panels'][0]['widgets'][0]['widget-data-visible-columns'] = visible_columns

# Let's make sure remark is in the columns list
if not any(c['column-key'] == 'remark' for c in columns):
    columns.append({
        "widget": "text",
        "column-key": "remark",
        "widget-type": "input",
        "widget-label": "Remark",
        "widget-readonly": False,
        "widget-data-path": "remark"
    })

data['panels'][0]['panels'][0]['widgets'][0]['widget-data-columns'] = columns

# Update DB
json_str = json.dumps(data)
json_str_escaped = json_str.replace("'", "''")

sql = f"UPDATE g2p_register_sections SET section_ui_schema = '{json_str_escaped}' WHERE section_id = 'cropsown_cultivation_details_section_01';"

subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres",
    "psql", "-U", "postgres", "-d", "cropsown", "-c", sql
])

# Update local file
sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"
with open(sql_file, 'r') as f:
    content = f.read()

pattern = rf"\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cultivation_details_section_01','c9ee1d48-93b5-52d5-a8fc-280266a39c10','FALSE','[^']+','[^']+','FALSE',0,'TRUE',10,'(\{{.*?\}})'"
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content[:match.start(1)] + json_str + content[match.end(1):]
    with open(sql_file, 'w') as f:
        f.write(content)
    print("Fixed!")
