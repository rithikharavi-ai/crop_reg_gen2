import json

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

# Instead of complex JSON parsing, let's just do a simpler search and replace for the exact JSON objects
# But JSON parsing is safer. Let's find the exact insert statement for cropsown_cropsown_record_section_01

import re

# find the JSON string inside the tuple
# ('uuid', 'uuid', 'cropsown_cropsown_record_section_01', ...)
pattern = r"\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cropsown_record_section_01','6b06a95a-9a6c-5a33-a33d-c1625716c59c','FALSE','cs_cropsown_record','Farmer Identity','FALSE',0,'FALSE',10,'(\{.*?\})'"

match = re.search(pattern, content, re.DOTALL)
if match:
    json_str = match.group(1)
    # The JSON string might contain escaped single quotes (e.g. '') but here it's simple
    try:
        data = json.loads(json_str)
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
                            
        new_json = json.dumps(data)
        # replace back
        content = content[:match.start(1)] + new_json + content[match.end(1):]
        with open(sql_file, 'w') as f:
            f.write(content)
        print("Success")
    except Exception as e:
        print("JSON Error", e)
else:
    print("Match not found")

