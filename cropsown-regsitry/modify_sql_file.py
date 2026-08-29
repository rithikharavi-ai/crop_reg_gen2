import json
import re

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

pattern = re.compile(r"(\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cluster_details_section_01'.*?')({.*?})(','FALSE','FALSE','FALSE','FALSE'\))")
match = pattern.search(content)

if not match:
    print("Could not find the target section in the SQL file.")
    exit(1)

prefix = match.group(1)
json_str = match.group(2)
suffix = match.group(3)

schema = json.loads(json_str)

new_fields = [
    {
        "widget": "text",
        "column-key": "region",
        "widget-type": "input",
        "widget-label": "Region",
        "widget-readonly": False,
        "widget-data-path": "region"
    },
    {
        "widget": "text",
        "column-key": "zone",
        "widget-type": "input",
        "widget-label": "Zone",
        "widget-readonly": False,
        "widget-data-path": "zone"
    },
    {
        "widget": "text",
        "column-key": "woreda",
        "widget-type": "input",
        "widget-label": "Woreda",
        "widget-readonly": False,
        "widget-data-path": "woreda"
    },
    {
        "widget": "text",
        "column-key": "kebele",
        "widget-type": "input",
        "widget-label": "Kebele",
        "widget-readonly": False,
        "widget-data-path": "kebele"
    },
    {
        "widget": "text",
        "column-key": "sub_kebele",
        "widget-type": "input",
        "widget-label": "Sub Kebele",
        "widget-readonly": False,
        "widget-data-path": "sub_kebele"
    }
]

# Find the dialog-table
found = False
for panel in schema.get('panels', []):
    for subpanel in panel.get('panels', []):
        for widget in subpanel.get('widgets', []):
            if widget.get('widget') == 'dialog-table':
                # Filter out existing fields to avoid duplication
                cols = widget.get('widget-data-columns', [])
                keys_to_add = {f['column-key'] for f in new_fields}
                
                cols = [c for c in cols if c.get('column-key') not in keys_to_add]
                
                # Insert the new fields at the end or right after land_id
                cols.extend(new_fields)
                widget['widget-data-columns'] = cols
                found = True

if found:
    new_json_str = json.dumps(schema, separators=(',', ':'))
    new_match_string = prefix + new_json_str + suffix
    
    new_content = content[:match.start()] + new_match_string + content[match.end():]
    
    with open(sql_file, 'w') as f:
        f.write(new_content)
    print("Successfully modified g2p_register_sections.sql!")
else:
    print("Could not find the dialog-table inside the JSON schema.")
