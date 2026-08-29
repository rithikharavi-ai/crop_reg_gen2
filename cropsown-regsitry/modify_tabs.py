import re
import uuid

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_ui_tab_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

# Remove the trailing semicolon
content = content.strip()
if content.endswith(';'):
    content = content[:-1]

survey_uuid = str(uuid.uuid4())
location_uuid = str(uuid.uuid4())

new_lines = f",\n('{survey_uuid}','6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cropsown_tab','cropsown_survey_personnel_section_02',20),\n('{location_uuid}','6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cropsown_tab','cropsown_cropsown_location_section_03',30);"

content += new_lines

with open(sql_file, 'w') as f:
    f.write(content)

print("Modified g2p_register_ui_tab_sections.sql successfully!")
