# Aaron Grincewicz
"""
Central configuration for data file locations.

All CSV data lives under a single ``data/`` directory (resolved relative to the
current working directory) to keep the project root tidy:

    data/
    ├── master_inventory.csv
    ├── master_stockroom_location.csv
    ├── unlocated_inventory.csv
    └── StockroomLocations/
        └── <CATEGORY-AISLE-COLUMN-ROW>.csv
"""
import sys
from pathlib import Path


def _resolve_base_dir() -> Path:
    """Return the base directory that should contain the ``data/`` folder.

    When running as a PyInstaller-frozen executable/app, CSV data must live in a
    writable location next to the executable (the app bundle itself is
    read-only). During normal development we fall back to the current working
    directory so the existing ``data/`` folder keeps working.
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd()


# Root directory that holds every CSV file used by the application.
DATA_DIR = _resolve_base_dir() / "data"

# Sub-directory holding the per-location stockroom CSV files.
LOCATIONS_DIR = DATA_DIR / "StockroomLocations"

# Top-level data files.
MASTER_INVENTORY_FILE = DATA_DIR / "master_inventory.csv"
UNLOCATED_INVENTORY_FILE = DATA_DIR / "unlocated_inventory.csv"
MASTER_STOCKROOM_FILE = DATA_DIR / "master_stockroom_location.csv"
