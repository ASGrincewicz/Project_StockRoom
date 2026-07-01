# Aaron Grincewicz — 02/19/2023
"""
Colorize Module

Provides helper functions for applying consistent color formatting to CLI output.
Uses the `colored` library to wrap text in ANSI color codes.

This module centralizes all color styling for the Stockroom system, ensuring:
- Consistent visual feedback
- Clear separation between presentation and business logic
- Easy updates to color themes if needed
"""

from colored import fg, bg, attr


def colorize_text_blue(text_to_colorize) -> str:
    """Return text formatted in blue."""
    return f"{fg(12)}{text_to_colorize}{attr(0)}"


def colorize_text_red(text_to_colorize) -> str:
    """Return text formatted in red (typically used for errors)."""
    return f"{fg(1)}{text_to_colorize}{attr(0)}"


def colorize_text_green(text_to_colorize) -> str:
    """Return text formatted in green (typically used for success messages)."""
    return f"{fg(10)}{text_to_colorize}{attr(0)}"


def colorize_text_salmon(text_to_colorize) -> str:
    """Return text formatted in salmon (used for section headers)."""
    return f"{fg(137)}{text_to_colorize}{attr(0)}"


def colorize_text_orange(text_to_colorize) -> str:
    """Return text formatted in orange (used for prompts and highlights)."""
    return f"{fg(214)}{text_to_colorize}{attr(0)}"


def colorize_location_status(text_to_colorize) -> str:
    """
    Colorize location status strings.

    If the text contains 'UNLOCATED', return red.
    Otherwise, return orange.
    """
    if "UNLOCATED" in text_to_colorize:
        return colorize_text_red(text_to_colorize)
    else:
        return colorize_text_orange(text_to_colorize)
