"""Source-keyed, human-reviewed Japanese translations.

Every module in this package exposes a TRANSLATIONS dictionary whose keys are
exact English source strings.  Keeping the English text as the key prevents a
later machine-translation pass from silently changing approved Japanese copy.
"""
from __future__ import annotations

from importlib import import_module
from pathlib import Path

STRICT_OVERRIDES: dict[str, str] = {}

for module_path in sorted(Path(__file__).parent.glob("*.py")):
    if module_path.stem.startswith("_"):
        continue
    module = import_module(f"japanese_strict.{module_path.stem}")
    STRICT_OVERRIDES.update(getattr(module, "TRANSLATIONS", {}))
