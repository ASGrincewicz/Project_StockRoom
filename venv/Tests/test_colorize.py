"""
Unit tests for the Colorize module.
"""
import pytest
import Colorize


class TestColorize:
    """Test cases for Colorize module."""
    
    def test_safe_text_with_string(self):
        """Test _safe_text with valid string."""
        result = Colorize._safe_text("Hello")
        assert result == "Hello"
    
    def test_safe_text_with_none(self):
        """Test _safe_text with None."""
        result = Colorize._safe_text(None)
        assert result == ""
    
    def test_safe_text_with_number(self):
        """Test _safe_text with numeric input."""
        result = Colorize._safe_text(42)
        assert result == "42"
    
    def test_safe_text_with_empty_string(self):
        """Test _safe_text with empty string."""
        result = Colorize._safe_text("")
        assert result == ""
    
    def test_colorize_blue(self):
        """Test blue color function."""
        result = Colorize.colorize_text_blue("test")
        assert "test" in result
        assert "\033[94m" in result  # Blue color code
        assert "\033[0m" in result   # Reset code
    
    def test_colorize_green(self):
        """Test green color function."""
        result = Colorize.colorize_text_green("test")
        assert "test" in result
        assert "\033[92m" in result  # Green color code
        assert "\033[0m" in result
    
    def test_colorize_red(self):
        """Test red color function."""
        result = Colorize.colorize_text_red("test")
        assert "test" in result
        assert "\033[91m" in result  # Red color code
        assert "\033[0m" in result
    
    def test_colorize_yellow(self):
        """Test yellow color function."""
        result = Colorize.colorize_text_yellow("test")
        assert "test" in result
        assert "\033[93m" in result  # Yellow color code
        assert "\033[0m" in result
    
    def test_colorize_orange(self):
        """Test orange color function."""
        result = Colorize.colorize_text_orange("test")
        assert "test" in result
        assert "\033[38;5;208m" in result  # Orange color code
        assert "\033[0m" in result
    
    def test_colorize_cyan(self):
        """Test cyan color function."""
        result = Colorize.colorize_text_cyan("test")
        assert "test" in result
        assert "\033[96m" in result  # Cyan color code
        assert "\033[0m" in result
    
    def test_colorize_magenta(self):
        """Test magenta color function."""
        result = Colorize.colorize_text_magenta("test")
        assert "test" in result
        assert "\033[95m" in result  # Magenta color code
        assert "\033[0m" in result
    
    def test_colorize_gray(self):
        """Test gray color function."""
        result = Colorize.colorize_text_gray("test")
        assert "test" in result
        assert "\033[90m" in result  # Gray color code
        assert "\033[0m" in result
    
    def test_colorize_white(self):
        """Test white color function."""
        result = Colorize.colorize_text_white("test")
        assert "test" in result
        assert "\033[97m" in result  # White color code
        assert "\033[0m" in result
    
    def test_colorize_salmon(self):
        """Test salmon color function."""
        result = Colorize.colorize_text_salmon("test")
        assert "test" in result
        assert "\033[38;5;210m" in result  # Salmon color code
        assert "\033[0m" in result
    
    def test_colorize_with_none(self):
        """Test colorize functions with None input."""
        result = Colorize.colorize_text_blue(None)
        assert result == "" or "\033[0m" in result
    
    def test_colorize_with_multiline_text(self):
        """Test colorize with multiline text."""
        text = "Line1\nLine2"
        result = Colorize.colorize_text_blue(text)
        assert "Line1" in result
        assert "Line2" in result
    
    def test_colorize_with_special_characters(self):
        """Test colorize with special characters."""
        text = "Test@#$%^&*()"
        result = Colorize.colorize_text_blue(text)
        assert text in result
    
    def test_colorize_nested_calls(self):
        """Test nested colorize calls."""
        # First colorize
        result1 = Colorize.colorize_text_blue("test")
        # Should still work when used in another colorize call
        result2 = Colorize.colorize_text_red(result1)
        assert "test" in result2
        assert "\033[91m" in result2
