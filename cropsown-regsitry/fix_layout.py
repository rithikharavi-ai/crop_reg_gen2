import json
import subprocess
import re

with open('schema_dump.json', 'r') as f:
    data = json.loads(f.read().strip())

# The raw widgets
farmer_photo = data['panels'][0]['panels'][0]['widgets'][0]
functional_record_id = data['panels'][0]['panels'][0]['widgets'][1]
fayda_fan_id = data['panels'][0]['panels'][0]['widgets'][2]

farmer_photo_upload = data['panels'][0]['panels'][1]['widgets'][0]
production_year = data['panels'][0]['panels'][1]['widgets'][1]
season = data['panels'][0]['panels'][1]['widgets'][2]

farmer_id = {
    "widget": "text",
    "widget-id": "farmer_id",
    "widget-type": "input",
    "widget-label": "Farmer ID",
    "widget-readonly": True,
    "widget-required": False,
    "widget-data-path": "6b06a95a-9a6c-5a33-a33d-c1625716c59c.farmer_id"
}

# Hide green text on photo
if 'widget-name-path' in farmer_photo:
    del farmer_photo['widget-name-path']
if 'widget-id-path' in farmer_photo:
    del farmer_photo['widget-id-path']
if 'widget-data-format' in farmer_photo:
    farmer_photo['widget-data-format']['showIdLabel'] = False

# Layout as requested
data['panels'][0]['panels'][0]['widgets'] = [farmer_photo]
data['panels'][0]['panels'][1]['widgets'] = [farmer_id, functional_record_id, fayda_fan_id]
data['panels'][0]['panels'][2]['widgets'] = [farmer_photo_upload, production_year, season]

json_str = json.dumps(data)
json_str_escaped = json_str.replace("'", "''")

sql = f"UPDATE g2p_register_sections SET section_ui_schema = '{json_str_escaped}' WHERE section_id = 'cropsown_cropsown_record_section_01';"

p = subprocess.run([
    "docker", "exec", "-i", "cropsown-registry-postgres",
    "psql", "-U", "postgres", "-d", "cropsown", "-c", sql
], capture_output=True, text=True)

print(p.stdout, p.stderr)

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"
with open(sql_file, 'r') as f:
    content = f.read()

pattern = rf"\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cropsown_record_section_01','6b06a95a-9a6c-5a33-a33d-c1625716c59c','FALSE','[^']+','[^']+','FALSE',0,'FALSE',10,'(\{{.*?\}})'"
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content[:match.start(1)] + json_str + content[match.end(1):]
    with open(sql_file, 'w') as f:
        f.write(content)
    print("Updated local file too!")

