"""
Unit tests for the Product module.
"""
import pytest
from Product import Product


class TestProduct:
    """Test cases for Product class."""
    
    def test_product_initialization_basic(self):
        """Test basic product initialization."""
        product = Product("WIDGET A", "1", 50)
        assert product.product_name == "WIDGET A"
        assert product.product_num == "0001"
        assert product.on_hand_count == 50
    
    def test_product_name_normalization(self):
        """Test that product names are normalized to uppercase."""
        product = Product("widget a", "1", 50)
        assert product.product_name == "WIDGET A"
    
    def test_product_name_stripping(self):
        """Test that product names are stripped of whitespace."""
        product = Product("  widget a  ", "1", 50)
        assert product.product_name == "WIDGET A"
    
    def test_product_name_empty_default(self):
        """Test that empty product name defaults to UNKNOWN."""
        product = Product("", "1", 50)
        assert product.product_name == "UNKNOWN"
    
    def test_product_name_none_default(self):
        """Test that None product name defaults to UNKNOWN."""
        product = Product(None, "1", 50)
        assert product.product_name == "UNKNOWN"
    
    def test_product_num_zero_padding(self):
        """Test that product numbers are zero-padded to 4 digits."""
        product1 = Product("WIDGET", "1", 50)
        assert product1.product_num == "0001"
        
        product2 = Product("WIDGET", "123", 50)
        assert product2.product_num == "0123"
        
        product3 = Product("WIDGET", "1234", 50)
        assert product3.product_num == "1234"
    
    def test_product_num_string_input(self):
        """Test that product numbers can be provided as strings."""
        product = Product("WIDGET", "42", 50)
        assert product.product_num == "0042"
    
    def test_product_num_invalid_default(self):
        """Test that invalid product number is handled gracefully."""
        product = Product("WIDGET", "INVALID", 50)
        # zfill on string keeps it as-is if not all digits
        assert product.product_num == "INVALID"
    
    def test_product_num_none_default(self):
        """Test that None product number is converted to string."""
        product = Product("WIDGET", None, 50)
        # None converts to "None" string, then zfill
        assert product.product_num == "None"
    
    def test_on_hand_count_integer(self):
        """Test that on-hand count is stored as integer."""
        product = Product("WIDGET", "1", 50)
        assert product.on_hand_count == 50
        assert isinstance(product.on_hand_count, int)
    
    def test_on_hand_count_string_conversion(self):
        """Test that string on-hand counts are converted to integers."""
        product = Product("WIDGET", "1", "75")
        assert product.on_hand_count == 75
    
    def test_on_hand_count_invalid_default(self):
        """Test that invalid on-hand count defaults to 0."""
        product = Product("WIDGET", "1", "INVALID")
        assert product.on_hand_count == 0
    
    def test_on_hand_count_none_default(self):
        """Test that None on-hand count defaults to 0."""
        product = Product("WIDGET", "1", None)
        assert product.on_hand_count == 0
    
    def test_product_with_all_invalid_inputs(self):
        """Test product initialization with all invalid inputs."""
        product = Product(None, "INVALID", "INVALID")
        assert product.product_name == "UNKNOWN"
        # "INVALID".zfill(4) returns "INVALID" since it's not numeric
        assert product.product_num == "INVALID"
        assert product.on_hand_count == 0
    
    def test_product_negative_count(self):
        """Test that negative counts are stored (inventory discrepancy tracking)."""
        product = Product("WIDGET", "1", -10)
        assert product.on_hand_count == -10
    
    def test_product_zero_count(self):
        """Test product with zero on-hand count."""
        product = Product("WIDGET", "1", 0)
        assert product.on_hand_count == 0
    
    def test_product_large_count(self):
        """Test product with large on-hand count."""
        product = Product("WIDGET", "1", 999999)
        assert product.on_hand_count == 999999
    
    def test_product_special_characters_in_name(self):
        """Test product with special characters in name."""
        product = Product("WIDGET-A@#$", "1", 50)
        assert product.product_name == "WIDGET-A@#$"
    
    def test_product_numeric_name(self):
        """Test product with numeric name."""
        product = Product("12345", "1", 50)
        assert product.product_name == "12345"
    
    def test_product_get_product_info(self, capsys):
        """Test get_product_info prints correctly."""
        product = Product("WIDGET", "42", 75)
        product.get_product_info()
        captured = capsys.readouterr()
        
        assert "Name: WIDGET" in captured.out
        assert "Product #: 0042" in captured.out
        assert "On Hand: 75" in captured.out
