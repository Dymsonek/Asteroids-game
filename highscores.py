import json
import os
from typing import Tuple


DEFAULT_FILE = "highscore.json"


def _storage_path(filename: str = DEFAULT_FILE) -> str:
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, filename)


def load_highscore() -> Tuple[str, int]:
    """Load high score and leader name from disk.

    Returns (name, score). If no file or invalid, returns ("", 0).
    """
    path = _storage_path()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        name = str(data.get("name", ""))
        score = int(data.get("score", 0))
        if score < 0:
            score = 0
        return name, score
    except Exception:
        return "", 0


def save_highscore(name: str, score: int) -> None:
    """Persist high score and leader name to disk.

    Only writes if score is non-negative; overwrites existing file.
    """
    score = max(0, int(score))
    data = {"name": name or "", "score": score}
    path = _storage_path()
    tmp_path = path + ".tmp"
    # Write atomically where possible
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    os.replace(tmp_path, path)

