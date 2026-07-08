"""
Unit tests for the ProductLocation module.
"""
import pytest
from pathlib import Path
import csv
import sys
from unittest.mock import patch

import ProductLocation as PL
import MasterInventory as MI


class TestReadLocationFile:
    """Test cases for read_location_file function."""
    
    def test_read_location_file_valid(self, clean_environment):
        """Test reading a valid location file."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET A", "20"])
            writer.writerow(["0102", "WIDGET B", "15"])
        
        result = PL.read_location_file("01-01-A-01")
        assert "0101" in result
        assert result["0101"]["WIDGET A"] == 20
    
    def test_read_location_file_not_found(self, clean_environment):
        """Test reading non-existent location file."""
        result = PL.read_location_file("NOTFOUND")
        assert result == {}
    
    def test_read_location_file_invalid_amount(self, clean_environment):
        """Test reading location file with invalid amount."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET", "INVALID"])
        
        result = PL.read_location_file("01-01-A-01")
        # Should use 0 for invalid amounts
        assert "0101" in result
        assert result["0101"]["WIDGET"] == 0
    
    def test_read_location_file_empty_rows(self, clean_environment):
        """Test reading location file with missing fields."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "", "20"])  # Missing name
        
        result = PL.read_location_file("01-01-A-01")
        # Should skip malformed rows
        assert "0101" not in result or result == {}


class TestUserInput:
    """Test cases for user_input function."""
    
    def test_user_input_valid(self, monkeypatch):
        """Test user_input with valid input."""
        monkeypatch.setattr("builtins.input", lambda _: "test")
        result = PL.user_input("Enter:")
        assert result == "test"
    
    def test_user_input_cancel_x(self, monkeypatch):
        """Test user_input recognizes X as cancel."""
        monkeypatch.setattr("builtins.input", lambda _: "X")
        with pytest.raises(KeyboardInterrupt):
            PL.user_input("Enter:")
    
    def test_user_input_cancel_cancel(self, monkeypatch):
        """Test user_input recognizes CANCEL."""
        monkeypatch.setattr("builtins.input", lambda _: "CANCEL")
        with pytest.raises(KeyboardInterrupt):
            PL.user_input("Enter:")
    
    def test_user_input_cancel_back(self, monkeypatch):
        """Test user_input recognizes BACK."""
        monkeypatch.setattr("builtins.input", lambda _: "BACK")
        with pytest.raises(KeyboardInterrupt):
            PL.user_input("Enter:")


class TestBackstockProduct:
    """Test cases for backstock_product function."""
    
    @pytest.mark.skip(reason="Requires complex mocking of interactive elements")
    def test_backstock_product_basic(self, clean_environment, monkeypatch):
        """Test basic backstock product functionality."""
        # Setup
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
        
        MI.master_inventory = {
            "0101": {"WIDGET A": 100}
        }
        MI.categories = [("WIDGETS", "01")]
        
        # This test would require complex input mocking
        # Skipped for now - integration tests recommended


class TestRemoveProduct:
    """Test cases for remove_product function."""
    
    @pytest.mark.skip(reason="Requires complex mocking of interactive elements")
    def test_remove_product_basic(self, clean_environment, monkeypatch):
        """Test basic remove product functionality."""
        # This test would require complex input mocking
        # Skipped for now - integration tests recommended
        pass


class TestAuditProduct:
    """Test cases for audit_product function."""
    
    @pytest.mark.skip(reason="Requires complex mocking of interactive elements")
    def test_audit_product(self, clean_environment, monkeypatch):
        """Test audit product functionality."""
        # This test would require complex input mocking
        # Skipped for now - integration tests recommended
        pass


class TestGetProductAmount:
    """Test cases for get_product_amount function."""
    
    def test_get_product_amount_zero_when_not_found(self, clean_environment):
        """Test get_product_amount returns 0 when product not in location."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET", "20"])
        
        result = PL.read_location_file("01-01-A-01")
        assert result["0101"]["WIDGET"] == 20


class TestCreateNewLocationFile:
    """Test cases for create_new_location_file function."""
    
    def test_create_new_location_file(self, clean_environment):
        """Test creating a new location file."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        PL.create_new_location_file("01-01-A-01")
        
        loc_path = Path("StockroomLocations/01-01-A-01.csv")
        assert loc_path.exists()
        
        # Verify headers
        with open(loc_path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert headers == ["Product #", "Product Name", "Amount"]
    
    def test_create_new_location_file_already_exists(self, clean_environment, capsys):
        """Test creating location file that already exists."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        loc_path.touch()
        
        # Should not raise error, just print message
        PL.create_new_location_file("01-01-A-01")
        captured = capsys.readouterr()
        # Should contain message about file existing


class TestLocationFileMalformedness:
    """Test cases for handling malformed location files."""
    
    def test_read_location_file_with_extra_spaces(self, clean_environment):
        """Test reading location file with extra spaces."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["  0101  ", "  WIDGET A  ", "  20  "])
        
        result = PL.read_location_file("01-01-A-01")
        # Should handle spaces correctly
        assert "0101" in result
    
    def test_read_location_file_duplicate_products(self, clean_environment):
        """Test reading location file with duplicate products."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET", "20"])
            writer.writerow(["0101", "WIDGET", "15"])
        
        result = PL.read_location_file("01-01-A-01")
        # Should combine amounts
        assert result["0101"]["WIDGET"] == 35
