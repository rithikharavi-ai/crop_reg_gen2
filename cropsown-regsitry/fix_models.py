import re

file_path = "/home/rithikharavi/Music/Gen2- crop-registry/cropsown-regsitry/cropsown-extension/src/openg2p_registry_cropsown_extension/register_domain/models/cluster.py"

with open(file_path, "r") as f:
    content = f.read()

# Remove the line `    sub_kebele: Mapped[str] = mapped_column(String, nullable=True)`
new_content = re.sub(r"    sub_kebele: Mapped\[str\] = mapped_column\(String, nullable=True\)\n", "", content)

with open(file_path, "w") as f:
    f.write(new_content)

print("Removed sub_kebele from cluster.py")
