import json
import re

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "cropsown_cropsown_record_section_01" in line:
        match = re.search(r"'({\".*?\"})'", line)
        if match:
            json_str = match.group(1)
            try:
                data = json.loads(json_str)
                
                # Traverse and remove widgets
                if 'panels' in data:
                    for panel1 in data['panels']:
                        if 'panels' in panel1:
                            for panel2 in panel1['panels']:
                                if 'widgets' in panel2:
                                    new_widgets = []
                                    for w in panel2['widgets']:
                                        w_id = w.get('widget-id', '')
                                        if w_id not in ['farmer_odk_ack_id', 'status', 'lifecycle_stage']:
                                            new_widgets.append(w)
                                    panel2['widgets'] = new_widgets
                                    
                new_json_str = json.dumps(data)
                # Escape single quotes in JSON string
                new_json_str = new_json_str.replace("'", "''")
                line = line[:match.start()] + "'" + new_json_str + "'" + line[match.end():]
            except json.JSONDecodeError as e:
                print("JSON parse error:", e)
    new_lines.append(line)

with open(sql_file, 'w') as f:
    f.writelines(new_lines)

print("Modified g2p_register_sections.sql successfully!")
