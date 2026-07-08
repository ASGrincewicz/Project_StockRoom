"""
Unit tests for the MasterStockRoom module.
"""
import pytest
from pathlib import Path
import csv
import sys
from unittest.mock import patch, MagicMock

# Import after setting path
import MasterStockRoom as MSR


class TestParseLocation:
    """Test cases for parse_location function."""
    
    def test_parse_location_valid_format(self):
        """Test parsing valid location format."""
        result = MSR.parse_location("01-02-A-03")
        assert result == ("01", "02", "A", "03")
    
    def test_parse_location_with_uppercase_column(self):
        """Test parsing location with uppercase column."""
        result = MSR.parse_location("01-05-Z-10")
        assert result == ("01", "05", "Z", "10")
    
    def test_parse_location_lowercase_converted(self):
        """Test parsing location with lowercase (stays as-is)."""
        result = MSR.parse_location("01-02-a-03")
        assert result == ("01", "02", "a", "03")
    
    def test_parse_location_invalid_too_few_parts(self):
        """Test parsing location with too few parts."""
        result = MSR.parse_location("01-02-A")
        assert result is None
    
    def test_parse_location_invalid_too_many_parts(self):
        """Test parsing location with too many parts."""
        result = MSR.parse_location("01-02-A-03-04")
        assert result is None
    
    def test_parse_location_empty_string(self):
        """Test parsing empty location string."""
        result = MSR.parse_location("")
        assert result is None


class TestComputeNextLocation:
    """Test cases for compute_next_location function."""
    
    def test_compute_next_location_empty_index(self):
        """Test computing next location when category is new."""
        index = {}
        category = ("WIDGETS", "01")
        result, message = MSR.compute_next_location(index, category)
        assert result == "01-01-A-01"
        assert message is None
    
    def test_compute_next_location_increment_row(self):
        """Test computing next location increments row."""
        index = {
            "01": {
                "01": {
                    "A": ["01"]
                }
            }
        }
        category = ("WIDGETS", "01")
        result, message = MSR.compute_next_location(index, category)
        assert result == "01-01-A-02"
    
    def test_compute_next_location_row_at_limit(self):
        """Test computing next location when row limit reached."""
        index = {
            "01": {
                "01": {
                    "A": ["20"]
                }
            }
        }
        category = ("WIDGETS", "01")
        result, message = MSR.compute_next_location(index, category, max_rows=20)
        assert result == "01-01-B-01"
        assert "Row limit reached" in message
    
    def test_compute_next_location_column_at_limit(self):
        """Test computing next location when column limit reached."""
        index = {
            "01": {
                "01": {
                    "J": ["20"]
                }
            }
        }
        category = ("WIDGETS", "01")
        result, message = MSR.compute_next_location(index, category, max_rows=20, max_columns=10)
        assert result == "01-02-A-01"
        assert "Column limit reached" in message
    
    def test_compute_next_location_aisle_at_limit(self):
        """Test computing next location when aisle limit reached."""
        index = {
            "01": {
                "30": {
                    "J": ["20"]
                }
            }
        }
        category = ("WIDGETS", "01")
        result, message = MSR.compute_next_location(index, category, max_aisles=30, max_columns=10)
        assert result is None
        assert "Aisle limit reached" in message


class TestSelectFromList:
    """Test cases for select_from_list function."""
    
    def test_select_from_list_existing_item(self, monkeypatch):
        """Test selecting existing item from list."""
        monkeypatch.setattr("builtins.input", lambda _: "1")
        result, is_new = MSR.select_from_list(["ITEM1", "ITEM2"], "Select:")
        assert result == "ITEM1"
        assert is_new is False
    
    def test_select_from_list_select_new(self, monkeypatch):
        """Test selecting NEW option."""
        monkeypatch.setattr("builtins.input", lambda _: "3")
        result, is_new = MSR.select_from_list(["ITEM1", "ITEM2"], "Select:")
        assert result is None
        assert is_new is True
    
    def test_select_from_list_invalid_retry(self, monkeypatch):
        """Test retry on invalid selection."""
        inputs = iter(["99", "0", "2"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result, is_new = MSR.select_from_list(["ITEM1", "ITEM2"], "Select:")
        assert result == "ITEM2"
        assert is_new is False
    
    def test_select_from_list_empty_list(self, monkeypatch):
        """Test with empty list."""
        monkeypatch.setattr("builtins.input", lambda _: "1")
        result, is_new = MSR.select_from_list([], "Select:")
        assert result is None
        assert is_new is True


class TestLocationIndex:
    """Test cases for location index building."""
    
    def test_build_location_index_empty_directory(self, clean_environment):
        """Test building index when no locations exist."""
        index = MSR.build_location_index()
        assert index == {}
    
    def test_build_location_index_with_files(self, clean_environment):
        """Test building index with location files."""
        loc_dir = Path("StockroomLocations")
        
        # Create sample location files
        Path("StockroomLocations/01-01-A-01.csv").touch()
        Path("StockroomLocations/01-01-A-02.csv").touch()
        Path("StockroomLocations/02-01-B-03.csv").touch()
        
        index = MSR.build_location_index()
        
        assert "01" in index
        assert "01" in index["01"]
        assert "A" in index["01"]["01"]
        assert "01" in index["01"]["01"]["A"]
        assert "02" in index["01"]["01"]["A"]


class TestUserInput:
    """Test cases for user_input function."""
    
    def test_user_input_valid(self, monkeypatch):
        """Test user_input with valid input."""
        monkeypatch.setattr("builtins.input", lambda _: "test input")
        result = MSR.user_input("Enter:")
        assert result == "test input"
    
    def test_user_input_strips_whitespace(self, monkeypatch):
        """Test user_input strips whitespace."""
        monkeypatch.setattr("builtins.input", lambda _: "  test input  ")
        result = MSR.user_input("Enter:")
        assert result == "test input"
    
    def test_user_input_cancel_x(self, monkeypatch):
        """Test user_input recognizes X as cancel."""
        monkeypatch.setattr("builtins.input", lambda _: "X")
        with pytest.raises(KeyboardInterrupt):
            MSR.user_input("Enter:")
    
    def test_user_input_cancel_cancel(self, monkeypatch):
        """Test user_input recognizes CANCEL as cancel."""
        monkeypatch.setattr("builtins.input", lambda _: "CANCEL")
        with pytest.raises(KeyboardInterrupt):
            MSR.user_input("Enter:")
    
    def test_user_input_cancel_back(self, monkeypatch):
        """Test user_input recognizes BACK as cancel."""
        monkeypatch.setattr("builtins.input", lambda _: "BACK")
        with pytest.raises(KeyboardInterrupt):
            MSR.user_input("Enter:")
    
    def test_user_input_cancel_lowercase(self, monkeypatch):
        """Test user_input recognizes lowercase cancel commands."""
        monkeypatch.setattr("builtins.input", lambda _: "x")
        with pytest.raises(KeyboardInterrupt):
            MSR.user_input("Enter:")


class TestCSVReadWrite:
    """Test cases for CSV read/write operations."""
    
    def test_read_from_stock_room_csv_valid(self, clean_environment, sample_stockroom_csv):
        """Test reading valid stockroom CSV."""
        MSR.read_from_stock_room_csv()
        assert len(MSR.categories) == 3
        assert ("WIDGETS", "01") in MSR.categories
        assert ("GADGETS", "02") in MSR.categories
    
    def test_read_from_stock_room_csv_not_found(self, clean_environment):
        """Test reading non-existent CSV."""
        result = MSR.read_from_stock_room_csv()
        assert result is None
    
    def test_write_to_stock_room_csv(self, clean_environment):
        """Test writing stockroom CSV."""
        MSR.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        MSR.write_to_stock_room_csv()
        
        # Verify file was created
        assert Path("master_stockroom_location.csv").exists()
        
        # Verify content
        with open("master_stockroom_location.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == 3  # header + 2 categories
            assert rows[0] == ["Category", "Code"]
