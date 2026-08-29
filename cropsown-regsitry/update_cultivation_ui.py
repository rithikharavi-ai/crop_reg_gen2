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

new_columns = []
for col in columns:
    if col['column-key'] == 'crop_category':
        new_columns.append(col)
        # Add new fields right after crop_category
        new_columns.extend([
            {
                "widget": "text",
                "column-key": "local_name",
                "widget-type": "input",
                "widget-label": "Local Name",
                "widget-readonly": False,
                "widget-data-path": "local_name"
            },
            {
                "widget": "text",
                "column-key": "scientific_name",
                "widget-type": "input",
                "widget-label": "Scientific Name",
                "widget-readonly": False,
                "widget-data-path": "scientific_name"
            },
            {
                "widget": "number",
                "column-key": "actual_yield",
                "widget-type": "input",
                "widget-label": "Actual Yield (quintal)",
                "widget-readonly": False,
                "widget-data-path": "actual_yield",
                "widget-data-format": {
                    "textAlign": "right",
                    "numericType": "decimal",
                    "thousandSeparator": ","
                }
            }
        ])
    elif col['column-key'] == 'land_prep_method':
        # Update to static options
        col['widget-data-source'] = {
            "type": "static",
            "options": [
                {"label": "Traditional Maresha Ploughing", "value": "traditional_maresha_ploughing"},
                {"label": "Tractor Disc/Moldboard Ploughing", "value": "tractor_disc_moldboard_ploughing"},
                {"label": "Manual Digging", "value": "manual_digging"},
                {"label": "Shilshalo", "value": "shilshalo"},
                {"label": "Ridging / Furrowing", "value": "ridging_furrowing"},
                {"label": "Manual leveling", "value": "manual_leveling"},
                {"label": "Soil & Water Conservation Structures", "value": "soil_water_conservation_structures"}
            ]
        }
        new_columns.append(col)
    elif col['column-key'] == 'cultivation_type':
        # Update to static options
        col['widget-data-source'] = {
            "type": "static",
            "options": [
                {"label": "Combine Harvester", "value": "combine_harvester"},
                {"label": "Combiner", "value": "combiner"},
                {"label": "Debo / Jigi", "value": "debo_jigi"},
                {"label": "Equine/Other Animals", "value": "equine_other"},
                {"label": "Family Labor", "value": "family_labor"},
                {"label": "Harvester", "value": "harvester"},
                {"label": "Hired Labor", "value": "hired_labor"},
                {"label": "Maize sheller", "value": "maize_sheller"},
                {"label": "Multi-Crop Trasher", "value": "multi_crop_trasher"},
                {"label": "Other", "value": "other"},
                {"label": "Oxen Ploughing + Manual Row Seeding", "value": "oxen_manual"},
                {"label": "Oxen Tillage", "value": "oxen_tillage"},
                {"label": "Planter", "value": "planter"},
                {"label": "Power Tiller", "value": "power_tiller"},
                {"label": "Rice polisher", "value": "rice_polisher"},
                {"label": "Thrashing Machine", "value": "thrashing_machine"},
                {"label": "Tractor", "value": "tractor"},
                {"label": "Tractor Ploughing", "value": "tractor_ploughing"},
                {"label": "Tractor Primary Tillage + Oxen Secondary Tillage", "value": "tractor_oxen"}
            ]
        }
        new_columns.append(col)
    else:
        new_columns.append(col)

data['panels'][0]['panels'][0]['widgets'][0]['widget-data-columns'] = new_columns

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

