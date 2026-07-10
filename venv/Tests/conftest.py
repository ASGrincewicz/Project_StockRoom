"""
Pytest configuration and fixtures for Project Stockroom test suite.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import csv
import sys

# Add parent directory (venv) to path for imports from main modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp = tempfile.mkdtemp()
    yield temp
    shutil.rmtree(temp)


@pytest.fixture
def sample_master_inventory_csv(temp_dir):
    """Create a sample master inventory CSV file."""
    data_dir = Path(temp_dir) / "data"
    data_dir.mkdir(exist_ok=True)
    csv_path = data_dir / "master_inventory.csv"
    data = [
        ["Product #", "Product Name", "On Hand Count"],
        ["0101", "WIDGET A", "50"],
        ["0102", "WIDGET B", "30"],
        ["0201", "GADGET X", "100"],
        ["0202", "GADGET Y", "25"],
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return csv_path


@pytest.fixture
def sample_stockroom_csv(temp_dir):
    """Create a sample stockroom location CSV file."""
    data_dir = Path(temp_dir) / "data"
    data_dir.mkdir(exist_ok=True)
    csv_path = data_dir / "master_stockroom_location.csv"
    data = [
        ["Category", "Code"],
        ["WIDGETS", "01"],
        ["GADGETS", "02"],
        ["TOOLS", "03"],
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return csv_path


@pytest.fixture
def sample_location_file(temp_dir):
    """Create a sample location file."""
    loc_dir = Path(temp_dir) / "data" / "StockroomLocations"
    loc_dir.mkdir(parents=True, exist_ok=True)
    
    loc_path = loc_dir / "01-01-A-01.csv"
    data = [
        ["Product #", "Product Name", "Amount"],
        ["0101", "WIDGET A", "20"],
        ["0102", "WIDGET B", "15"],
    ]
    with open(loc_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return loc_path


@pytest.fixture
def clean_environment(monkeypatch, temp_dir):
    """Set up a clean test environment."""
    # Change to temp directory
    monkeypatch.chdir(temp_dir)
    
    # Create directories (all CSV data lives under data/)
    loc_dir = Path(temp_dir) / "data" / "StockroomLocations"
    loc_dir.mkdir(parents=True, exist_ok=True)
    
    yield temp_dir
