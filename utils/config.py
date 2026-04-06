BASE_URL = "https://mb.io/en-AE"
import json
from pathlib import Path


def load_nav_data():
    """
    Reads the navigation_data.json file from the data folder.
    """
    root_dir = Path(__file__).resolve().parent.parent
    data_path = root_dir / "data" / "navigation_data.json"

    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)