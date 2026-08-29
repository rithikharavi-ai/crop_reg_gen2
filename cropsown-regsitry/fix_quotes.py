import re

sql_file = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/meta_data/register-metadata/g2p_register_sections.sql"

with open(sql_file, 'r') as f:
    content = f.read()

# We need to find the place where it says 10,{"panels" and change it to 10,'{"panels"
# And then find },"widget-data-dialog-title-edit":"Edit Cluster"}],"panel-id":"vertical_panel_cs_cluster_details_1","panel-orientation":"vertical"}],"panel-id":"horizontal_panel_cs_cluster_details","panel-orientation":"horizontal"}],"section-id":"cropsown_cluster_details_section_01","section-title":"Cluster Information Details","section-editable":true}','FALSE','FALSE','FALSE','FALSE')
# and add a ' at the end of the JSON block.

content = content.replace("10,{\"panels\"", "10,'{\"panels\"")
content = content.replace("\"section-editable\":true}','FALSE','FALSE','FALSE','FALSE')", "\"section-editable\":true}','FALSE','FALSE','FALSE','FALSE')") # wait, the end of the json is before ','FALSE'

# Let's see exactly what follows the json block in my previous script:
# The regex was ('cropsown_cluster_details_section_01'.*?,'\{.*?\})(','FALSE')
# So it ended right after the } and match.group(2) was ','FALSE'
# So I just need to replace },'FALSE' with }','FALSE'

content = content.replace("\"section-editable\":true},'FALSE'", "\"section-editable\":true}','FALSE'")

with open(sql_file, 'w') as f:
    f.write(content)
