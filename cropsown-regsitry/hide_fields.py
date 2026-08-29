import json
import re

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

pattern = re.compile(r"(\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cropsown_record_section_01'.*?')({.*?})(','FALSE','FALSE','FALSE','FALSE'\))")
match = pattern.search(content)

if match:
    prefix = match.group(1)
    json_str = match.group(2)
    suffix = match.group(3)

    schema = json.loads(json_str)
    
    fields_to_make_readonly = ["farmer_odk_ack_id", "status", "production_year", "season", "lifecycle_stage"]
    
    for panel in schema.get('panels', []):
        for subpanel in panel.get('panels', []):
            if 'widgets' in subpanel:
                for w in subpanel['widgets']:
                    if w.get('widget-id') in fields_to_make_readonly:
                        w['widget-readonly'] = True

    new_json_str = json.dumps(schema, separators=(',', ':'))
    new_match_string = prefix + new_json_str + suffix
    new_content = content[:match.start()] + new_match_string + content[match.end():]
    
    with open(sql_file, 'w') as f:
        f.write(new_content)
    print("Modified Farmer Identity section successfully!")
else:
    print("Could not find section.")
