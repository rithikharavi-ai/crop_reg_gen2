"""Guard: the lifecycle constants used by the service must match the model enums.

`domain_lifecycle_utils` declares the stage and state names as plain strings to
avoid a models -> services -> models import cycle. That duplication is only safe
while the two agree, so this test compares them.
"""

import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent.parent / "cropsown-extension/src/openg2p_registry_cropsown_extension/register_domain"


def _members(path, class_name):
    src = (SRC / path).read_text()
    block = re.search(r"class %s\([^)]*\):\n((?:\s+.*\n)+?)(?=\n\S|\nclass )" % class_name, src)
    assert block, f"{class_name} not found in {path}"
    return dict(re.findall(r'^\s+([A-Z_]+)\s*=\s*"([^"]+)"', block.group(1), re.M))


def test_lifecycle_constants_match_the_model_enums():
    for cls in ("LifecycleStageEnum", "StageStateEnum", "RejectedAtStageEnum"):
        model = _members("models/enums.py", cls)
        service = _members("services/domain_lifecycle_utils.py", cls)
        assert model == service, (
            f"{cls} has drifted between models/enums.py and "
            f"services/domain_lifecycle_utils.py:\n  model  : {model}\n  service: {service}"
        )
