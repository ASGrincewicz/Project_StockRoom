"""
Unit tests for the MasterInventory module.
"""
import pytest
from pathlib import Path
import csv
import sys
from unittest.mock import patch
import tempfile
import shutil

import MasterInventory as MI
import MasterStockRoom as MSR


class TestProductNumberVerification:
    """Test cases for verify_prod_num function."""
    
    def test_verify_prod_num_all_new(self):
        """Test verify_prod_num returns True for all new numbers."""
        MI.master_inventory = {}
        result = MI.verify_prod_num(["0001", "0002", "0003"])
        assert result is True
    
    def test_verify_prod_num_one_exists(self):
        """Test verify_prod_num returns False if any exists."""
        MI.master_inventory = {"0001": {"WIDGET": 50}}
        result = MI.verify_prod_num(["0001", "0002"])
        assert result is False
    
    def test_verify_prod_num_all_exist(self):
        """Test verify_prod_num returns False if all exist."""
        MI.master_inventory = {"0001": {"WIDGET": 50}, "0002": {"GADGET": 30}}
        result = MI.verify_prod_num(["0001", "0002"])
        assert result is False


class TestGetCategoryName:
    """Test cases for get_category_name function."""
    
    def test_get_category_name_exists(self):
        """Test getting category name for existing code."""
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        result = MI.get_category_name("01")
        assert result == "WIDGETS"
    
    def test_get_category_name_not_found(self):
        """Test getting category name for non-existent code."""
        MI.categories = [("WIDGETS", "01")]
        result = MI.get_category_name("99")
        assert result == "UNKNOWN"


class TestGetCategoryCode:
    """Test cases for get_category_code function."""
    
    def test_get_category_code_exists(self):
        """Test getting category code for existing name."""
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        result = MI.get_category_code("WIDGETS")
        assert result == "01"
    
    def test_get_category_code_not_found(self):
        """Test getting category code for non-existent name."""
        MI.categories = [("WIDGETS", "01")]
        result = MI.get_category_code("TOOLS")
        assert result is None


class TestGetBackstockLocations:
    """Test cases for get_backstock_locations function."""
    
    def test_get_backstock_locations_empty_directory(self, clean_environment):
        """Test getting backstock locations when directory is empty."""
        locs, total = MI.get_backstock_locations("0101")
        assert locs == []
        assert total == 0
    
    def test_get_backstock_locations_with_products(self, clean_environment):
        """Test getting backstock locations with products."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        # Create location files
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET", "20"])
            writer.writerow(["0102", "OTHER", "10"])
        
        locs, total = MI.get_backstock_locations("0101")
        assert len(locs) > 0
        assert total > 0


class TestSortInventory:
    """Test cases for sort_inventory_by_prod_num function."""
    
    def test_sort_inventory_empty(self):
        """Test sorting empty inventory."""
        MI.master_inventory = {}
        result = MI.sort_inventory_by_prod_num()
        assert result == []
    
    def test_sort_inventory_single_item(self):
        """Test sorting inventory with single item."""
        MI.master_inventory = {"0001": {"WIDGET": 50}}
        result = MI.sort_inventory_by_prod_num()
        assert result == ["0001"]
    
    def test_sort_inventory_multiple_items(self):
        """Test sorting inventory with multiple items."""
        MI.master_inventory = {
            "0003": {"ITEM3": 30},
            "0001": {"ITEM1": 50},
            "0002": {"ITEM2": 20}
        }
        result = MI.sort_inventory_by_prod_num()
        assert result == ["0001", "0002", "0003"]


class TestCategoryManagement:
    """Test cases for category management functions."""
    
    def test_set_categories(self, monkeypatch):
        """Test setting categories interactively."""
        MI.categories = []
        inputs = iter(["WIDGETS", "GADGETS", "DONE"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        
        MI.set_categories()
        assert len(MI.categories) == 2
        assert ("WIDGETS", "01") in MI.categories
    
    def test_add_categories_new(self, monkeypatch):
        """Test adding new categories."""
        MI.categories = [("EXISTING", "01")]
        inputs = iter(["NEW_CAT", "DONE"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        
        MI.add_categories()
        assert ("NEW_CAT", "02") in MI.categories
    
    def test_add_categories_duplicate(self, monkeypatch):
        """Test adding duplicate category is skipped."""
        MI.categories = [("WIDGETS", "01")]
        inputs = iter(["WIDGETS", "GADGETS", "DONE"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        
        MI.add_categories()
        # Should have WIDGETS + GADGETS
        assert len(MI.categories) == 2
    
    def test_show_categories_with_data(self, capsys):
        """Test showing categories."""
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        MI.show_categories()
        captured = capsys.readouterr()
        assert "WIDGETS" in captured.out
        assert "GADGETS" in captured.out
    
    def test_show_categories_empty(self, capsys):
        """Test showing categories when empty."""
        MI.categories = []
        MI.show_categories()
        captured = capsys.readouterr()
        assert "No categories" in captured.out


class TestGetNextProductNumber:
    """Test cases for get_next_product_number function."""
    
    def test_get_next_product_number_first_in_category(self, clean_environment, sample_master_inventory_csv):
        """Test getting first product number in category."""
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        result = MI.get_next_product_number("WIDGETS")
        # Should be 0103 (after 0101, 0102)
        assert result.startswith("01")
    
    def test_get_next_product_number_invalid_category(self, clean_environment, sample_master_inventory_csv):
        """Test getting product number for invalid category."""
        MI.categories = [("WIDGETS", "01")]
        result = MI.get_next_product_number("INVALID")
        assert result is None


class TestCSVReadWrite:
    """Test cases for CSV read/write operations."""
    
    def test_read_from_master_inventory_csv(self, clean_environment, sample_master_inventory_csv):
        """Test reading master inventory CSV."""
        MI.master_inventory = {}
        MI.read_from_master_inventory_csv()
        
        assert "0101" in MI.master_inventory
        assert "0102" in MI.master_inventory
    
    def test_write_to_master_inventory_csv(self, clean_environment):
        """Test writing master inventory CSV."""
        MI.master_inventory = {
            "0001": {"WIDGET A": 50},
            "0002": {"WIDGET B": 30}
        }
        MI.file_contents_read = True
        
        MI.write_to_master_inventory_csv()
        
        # Verify file exists
        assert Path("master_inventory.csv").exists()
        
        # Verify content
        with open("master_inventory.csv", "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2


class TestProductSelection:
    """Test cases for product selection functions."""
    
    def test_select_product_interactively(self, monkeypatch):
        """Test interactive product selection."""
        MI.master_inventory = {
            "0001": {"WIDGET A": 50},
            "0002": {"WIDGET B": 30},
            "0003": {"GADGET X": 100}
        }
        inputs = iter(["WIDGET", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        
        result = MI.select_product_interactively()
        assert result is not None
        num, name = result
        assert num == "0001"
    
    def test_select_product_no_matches(self, monkeypatch):
        """Test product selection with no matches."""
        MI.master_inventory = {"0001": {"WIDGET": 50}}
        monkeypatch.setattr("builtins.input", lambda _: "NOTFOUND")
        
        result = MI.select_product_interactively()
        assert result is None


class TestShowProductsInCategory:
    """Test cases for showing products in category."""
    
    def test_show_products_in_category(self, monkeypatch, capsys):
        """Test showing products in category."""
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        MI.master_inventory = {
            "0101": {"WIDGET A": 50},
            "0102": {"WIDGET B": 30},
            "0201": {"GADGET X": 100}
        }
        
        inputs = iter(["1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        
        MI.show_products_in_category()
        captured = capsys.readouterr()
        
        assert "WIDGET A" in captured.out
        assert "WIDGET B" in captured.out
