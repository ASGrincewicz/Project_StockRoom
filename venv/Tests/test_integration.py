"""
Integration tests for Project Stockroom.
Tests workflows that span multiple modules.
"""
import pytest
from pathlib import Path
import csv
import sys

import MasterInventory as MI
import MasterStockRoom as MSR
import ProductLocation as PL
from Product import Product


class TestInventoryWorkflow:
    """Integration tests for inventory workflows."""
    
    def test_create_and_read_inventory(self, clean_environment):
        """Test creating and reading inventory."""
        # Create inventory
        MI.master_inventory = {
            "0101": {"WIDGET A": 50},
            "0102": {"WIDGET B": 30},
            "0201": {"GADGET X": 100}
        }
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        MI.file_contents_read = True
        
        # Write to file
        MI.write_to_master_inventory_csv()
        
        # Verify file exists and has correct content
        assert Path("master_inventory.csv").exists()
        
        # Clear and read back
        MI.master_inventory = {}
        MI.read_from_master_inventory_csv()
        
        assert "0101" in MI.master_inventory
        assert "0102" in MI.master_inventory
    
    def test_category_management_workflow(self, clean_environment, monkeypatch):
        """Test complete category management workflow."""
        MI.categories = []
        
        # Set categories in MI
        inputs = iter(["WIDGETS", "GADGETS", "TOOLS", "DONE"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        MI.set_categories()
        
        # Verify categories were set
        assert len(MI.categories) == 3
        
        # Write to file
        MSR.write_to_stock_room_csv()
        
        # Verify file was created
        assert Path("master_stockroom_location.csv").exists()


class TestLocationWorkflow:
    """Integration tests for location workflows."""
    
    def test_create_and_populate_location(self, clean_environment):
        """Test creating and populating a location."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        # Create location file
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET A", "20"])
            writer.writerow(["0102", "WIDGET B", "15"])
        
        # Read it back
        products = PL.read_location_file("01-01-A-01")
        
        assert "0101" in products
        assert products["0101"]["WIDGET A"] == 20
    
    def test_multiple_location_index(self, clean_environment):
        """Test building index with multiple locations."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        # Create multiple location files
        locations = [
            "01-01-A-01.csv",
            "01-01-A-02.csv",
            "01-01-B-01.csv",
            "02-01-A-01.csv"
        ]
        
        for loc in locations:
            Path(f"StockroomLocations/{loc}").touch()
        
        # Build index
        index = MSR.build_location_index()
        
        assert "01" in index
        assert "02" in index
        assert "01" in index["01"]  # Aisle
        assert "A" in index["01"]["01"]  # Column


class TestProductWorkflow:
    """Integration tests for product workflows."""
    
    def test_product_creation_and_storage(self, clean_environment):
        """Test creating products and storing in inventory."""
        # Create products
        p1 = Product("Widget A", "101", 50)
        p2 = Product("Widget B", "102", 30)
        
        # Store in inventory
        MI.master_inventory = {
            p1.product_num: {p1.product_name: p1.on_hand_count},
            p2.product_num: {p2.product_name: p2.on_hand_count}
        }
        
        # Verify retrieval
        assert "0101" in MI.master_inventory
        assert "0102" in MI.master_inventory
        
        # Sort should work
        sorted_nums = MI.sort_inventory_by_prod_num()
        assert sorted_nums == ["0101", "0102"]
    
    def test_product_search_and_display(self, clean_environment, capsys):
        """Test searching for products and displaying info."""
        # Setup inventory
        MI.master_inventory = {
            "0101": {"WIDGET A": 50},
            "0102": {"WIDGET B": 30}
        }
        MI.categories = [("WIDGETS", "01")]
        
        # Get product info
        product = Product("WIDGET A", "0101", 50)
        product.get_product_info()
        
        captured = capsys.readouterr()
        assert "WIDGET A" in captured.out
        assert "0101" in captured.out
        assert "50" in captured.out


class TestFullWorkflow:
    """Integration tests for full end-to-end workflows."""
    
    def test_complete_stock_management_workflow(self, clean_environment):
        """Test complete stock management workflow."""
        # 1. Create categories
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        MSR.categories = MI.categories
        
        # 2. Create inventory
        MI.master_inventory = {
            "0101": {"WIDGET A": 100},
            "0102": {"WIDGET B": 50},
            "0201": {"GADGET X": 75}
        }
        
        # 3. Save everything
        MI.file_contents_read = True
        MI.write_to_master_inventory_csv()
        MSR.write_to_stock_room_csv()
        
        # 4. Create locations
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product #", "Product Name", "Amount"])
            writer.writerow(["0101", "WIDGET A", "40"])
            writer.writerow(["0102", "WIDGET B", "20"])
        
        # 5. Verify everything works
        assert Path("master_inventory.csv").exists()
        assert Path("master_stockroom_location.csv").exists()
        assert Path("StockroomLocations/01-01-A-01.csv").exists()
        
        # 6. Reload and verify
        MI.master_inventory = {}
        MI.read_from_master_inventory_csv()
        
        assert "0101" in MI.master_inventory
        assert "0201" in MI.master_inventory
        
        # 7. Test backstock query
        locs, total = MI.get_backstock_locations("0101")
        assert total > 0
    
    def test_location_listing_workflow(self, clean_environment):
        """Test location listing and navigation."""
        MI.categories = [("WIDGETS", "01"), ("GADGETS", "02")]
        
        # Create a variety of locations
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        locations = [
            "01-01-A-01.csv",  # Category 01, Aisle 01
            "01-01-A-02.csv",  # Category 01, Aisle 01
            "01-02-B-01.csv",  # Category 01, Aisle 02
            "02-01-A-01.csv",  # Category 02, Aisle 01
        ]
        
        for loc in locations:
            Path(f"StockroomLocations/{loc}").touch()
        
        # Build and verify index
        index = MSR.build_location_index()
        
        # Should have both categories
        assert "01" in index
        assert "02" in index
        
        # Category 01 should have 2 aisles
        assert "01" in index["01"]
        assert "02" in index["01"]
        
        # Aisle 01, Column A should have 2 rows
        assert "01" in index["01"]["01"]["A"]
        assert "02" in index["01"]["01"]["A"]


class TestErrorHandling:
    """Integration tests for error handling."""
    
    def test_invalid_csv_graceful_handling(self, clean_environment):
        """Test graceful handling of invalid CSV files."""
        MI.master_inventory = {}
        
        # Create malformed CSV
        with open("master_inventory.csv", "w") as f:
            f.write("Not,Proper,CSV\nMalformed,Data")
        
        # Should not crash
        MI.read_from_master_inventory_csv()
        # Inventory should be empty or partially loaded
        assert isinstance(MI.master_inventory, dict)
    
    def test_missing_file_graceful_handling(self, clean_environment):
        """Test graceful handling of missing files."""
        # Should not crash
        MI.read_from_master_inventory_csv()
        assert isinstance(MI.master_inventory, dict)
        
        MSR.read_from_stock_room_csv()
        assert isinstance(MSR.categories, list)
    
    def test_corrupted_location_file_handling(self, clean_environment):
        """Test handling of corrupted location files."""
        loc_dir = Path("StockroomLocations")
        loc_dir.mkdir(exist_ok=True)
        
        # Create file with invalid data
        loc_path = loc_dir / "01-01-A-01.csv"
        with open(loc_path, "w", newline="") as f:
            f.write("This is not CSV format\nComplete junk\n!")
        
        # Should handle gracefully
        result = PL.read_location_file("01-01-A-01")
        assert isinstance(result, dict)
