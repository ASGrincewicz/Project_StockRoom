"""
Unit tests for the Messages module.
"""
import pytest
import Messages as MSG
import Colorize


class TestMessages:
    """Test cases for Messages module."""
    
    def test_file_exist_message(self):
        """Test file_exist message."""
        result = MSG.file_exist()
        assert "already exists" in result.lower()
        # Should contain color codes
        assert "\033[" in result
    
    def test_file_not_found_message(self):
        """Test file_not_found message."""
        result = MSG.file_not_found()
        assert "not found" in result.lower()
        assert "\033[" in result
    
    def test_location_empty_message(self):
        """Test location_empty message."""
        result = MSG.location_empty()
        assert "empty" in result.lower() or "no products" in result.lower()
        assert "\033[" in result
    
    def test_product_not_found_message(self):
        """Test product_not_found message."""
        result = MSG.product_not_found()
        assert "not found" in result.lower()
        assert "\033[" in result
    
    def test_invalid_input_default(self):
        """Test invalid_input with default message."""
        result = MSG.invalid_input()
        assert "invalid" in result.lower()
        assert "\033[" in result
    
    def test_invalid_input_custom_message(self):
        """Test invalid_input with custom message."""
        custom_msg = "Custom error message"
        result = MSG.invalid_input(custom_msg)
        assert custom_msg in result
        assert "\033[" in result
    
    def test_get_location_input(self, monkeypatch):
        """Test get_location_input with valid input."""
        monkeypatch.setattr("builtins.input", lambda _: "LOC-01-A-01")
        result = MSG.get_location_input()
        assert result == "LOC-01-A-01"
    
    def test_get_location_input_with_spaces(self, monkeypatch):
        """Test get_location_input strips spaces."""
        monkeypatch.setattr("builtins.input", lambda _: "  LOC-01-A-01  ")
        result = MSG.get_location_input()
        assert result == "LOC-01-A-01"
    
    def test_get_location_input_uppercase(self, monkeypatch):
        """Test get_location_input converts to uppercase."""
        monkeypatch.setattr("builtins.input", lambda _: "loc-01-a-01")
        result = MSG.get_location_input()
        assert result == "LOC-01-A-01"
    
    def test_get_location_input_empty_retry(self, monkeypatch):
        """Test get_location_input retries on empty input."""
        inputs = iter(["", "", "VALID-LOC"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_location_input()
        assert result == "VALID-LOC"
    
    def test_get_prod_num_input_valid(self, monkeypatch):
        """Test get_prod_num_input with valid numeric input."""
        monkeypatch.setattr("builtins.input", lambda _: "123")
        result = MSG.get_prod_num_input()
        assert result == "0123"
    
    def test_get_prod_num_input_zero_padding(self, monkeypatch):
        """Test get_prod_num_input applies zero padding."""
        monkeypatch.setattr("builtins.input", lambda _: "1")
        result = MSG.get_prod_num_input()
        assert result == "0001"
    
    def test_get_prod_num_input_invalid_retry(self, monkeypatch):
        """Test get_prod_num_input retries on non-digit input."""
        inputs = iter(["ABC", "!@#", "42"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_prod_num_input()
        assert result == "0042"
    
    def test_get_amount_input_positive(self, monkeypatch):
        """Test get_amount_input with positive value."""
        monkeypatch.setattr("builtins.input", lambda _: "50")
        result = MSG.get_amount_input(allow_negative=False)
        assert result == 50
    
    def test_get_amount_input_zero(self, monkeypatch):
        """Test get_amount_input with zero."""
        monkeypatch.setattr("builtins.input", lambda _: "0")
        result = MSG.get_amount_input(allow_negative=False)
        assert result == 0
    
    def test_get_amount_input_negative_not_allowed(self, monkeypatch):
        """Test get_amount_input rejects negative when not allowed."""
        inputs = iter(["-10", "20"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_amount_input(allow_negative=False)
        assert result == 20
    
    def test_get_amount_input_negative_allowed(self, monkeypatch):
        """Test get_amount_input accepts negative when allowed."""
        monkeypatch.setattr("builtins.input", lambda _: "-15")
        result = MSG.get_amount_input(allow_negative=True)
        assert result == -15
    
    def test_get_amount_input_invalid_retry(self, monkeypatch):
        """Test get_amount_input retries on non-numeric input."""
        inputs = iter(["ABC", "12.5", "100"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_amount_input(allow_negative=False)
        assert result == 100
    
    def test_get_category_input_valid(self, monkeypatch):
        """Test get_category_input with valid input."""
        monkeypatch.setattr("builtins.input", lambda _: "WIDGETS")
        result = MSG.get_category_input()
        assert result == "WIDGETS"
    
    def test_get_category_input_uppercase(self, monkeypatch):
        """Test get_category_input converts to uppercase."""
        monkeypatch.setattr("builtins.input", lambda _: "widgets")
        result = MSG.get_category_input()
        assert result == "WIDGETS"
    
    def test_get_category_input_strips_spaces(self, monkeypatch):
        """Test get_category_input strips spaces."""
        monkeypatch.setattr("builtins.input", lambda _: "  WIDGETS  ")
        result = MSG.get_category_input()
        assert result == "WIDGETS"
    
    def test_get_category_input_empty_retry(self, monkeypatch):
        """Test get_category_input retries on empty input."""
        inputs = iter(["", "  ", "GADGETS"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_category_input()
        assert result == "GADGETS"
    
    def test_get_range_input_valid(self, monkeypatch):
        """Test get_range_input with valid range."""
        monkeypatch.setattr("builtins.input", lambda _: "1-10")
        result = MSG.get_range_input()
        assert result == (1, 10)
    
    def test_get_range_input_large_range(self, monkeypatch):
        """Test get_range_input with large range."""
        monkeypatch.setattr("builtins.input", lambda _: "100-999")
        result = MSG.get_range_input()
        assert result == (100, 999)
    
    def test_get_range_input_invalid_format_retry(self, monkeypatch):
        """Test get_range_input retries on invalid format."""
        inputs = iter(["1_10", "1 10", "5-20"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_range_input()
        assert result == (5, 20)
    
    def test_get_range_input_invalid_values_retry(self, monkeypatch):
        """Test get_range_input retries on non-numeric values."""
        inputs = iter(["A-B", "1-20"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_range_input()
        assert result == (1, 20)
    
    def test_get_range_input_reversed_range_retry(self, monkeypatch):
        """Test get_range_input retries when start > end."""
        inputs = iter(["20-1", "1-20"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.get_range_input()
        assert result == (1, 20)
    
    def test_confirm_action_yes(self, monkeypatch):
        """Test confirm_action with Y response."""
        monkeypatch.setattr("builtins.input", lambda _: "Y")
        result = MSG.confirm_action()
        assert result == "Y"
    
    def test_confirm_action_no(self, monkeypatch):
        """Test confirm_action with N response."""
        monkeypatch.setattr("builtins.input", lambda _: "N")
        result = MSG.confirm_action()
        assert result == "N"
    
    def test_confirm_action_lowercase(self, monkeypatch):
        """Test confirm_action converts lowercase to uppercase."""
        monkeypatch.setattr("builtins.input", lambda _: "y")
        result = MSG.confirm_action()
        assert result == "Y"
    
    def test_confirm_action_custom_prompt(self, monkeypatch):
        """Test confirm_action with custom prompt."""
        monkeypatch.setattr("builtins.input", lambda _: "Y")
        result = MSG.confirm_action("Custom prompt?\n")
        assert result == "Y"
    
    def test_confirm_action_invalid_retry(self, monkeypatch):
        """Test confirm_action retries on invalid input."""
        inputs = iter(["X", "1", "Y"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        result = MSG.confirm_action()
        assert result == "Y"
