import re

file_path = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/register_domain/schemas/cluster.py"

with open(file_path, "r") as f:
    content = f.read()

# Add the new fields
new_fields = """    region: Optional[str] = None
    zone: Optional[str] = None
    woreda: Optional[str] = None
    kebele: Optional[str] = None
    sub_kebele: Optional[str] = None
"""
# Replace sub_kebele if it exists to avoid duplicates
content = re.sub(r"    sub_kebele: Optional\[str\] = None\n", "", content)

# Insert after is_land_registered
content = re.sub(
    r"(    is_land_registered: Optional\[bool\] = None\n)",
    r"\1" + new_fields,
    content
)

with open(file_path, "w") as f:
    f.write(content)

print("Added fields to schema")
