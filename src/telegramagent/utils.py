from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(f: str | Path) -> Any:
    path = Path(f)
    if path.suffix != ".json":
        raise ValueError(f"File {f} is not a json file")

    with open(path) as fp:
        return json.load(fp)
