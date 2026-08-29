import subprocess

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

import re
pattern = re.compile(r"(\('6b06a95a-9a6c-5a33-a33d-c1625716c59c','cropsown_cluster_details_section_01'.*?'FALSE','FALSE','FALSE','FALSE'\))")
match = pattern.search(content)

if match:
    values = match.group(1)
    insert_sql = f'INSERT INTO g2p_register_sections VALUES {values};'
    
    subprocess.run(["docker", "exec", "-i", "cropsown-registry-postgres", "psql", "-U", "postgres", "-d", "cropsown"], input=insert_sql.encode())
    print("Done")
else:
    print("Could not find the row")
