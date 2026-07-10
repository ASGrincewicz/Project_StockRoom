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
from pathlib import Path

# Root directory that holds every CSV file used by the application.
DATA_DIR = Path("data")

# Sub-directory holding the per-location stockroom CSV files.
LOCATIONS_DIR = DATA_DIR / "StockroomLocations"

# Top-level data files.
MASTER_INVENTORY_FILE = DATA_DIR / "master_inventory.csv"
UNLOCATED_INVENTORY_FILE = DATA_DIR / "unlocated_inventory.csv"
MASTER_STOCKROOM_FILE = DATA_DIR / "master_stockroom_location.csv"
