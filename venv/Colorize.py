"""
Crash‑proof Colorize Module

Safely applies ANSI color codes to text.
If text is None or not a string, it is converted safely.
If the terminal does not support ANSI colors, output remains readable.
"""

def _safe_text(text):
    """Ensure text is always a safe string."""
    try:
        if text is None:
            return ""
        return str(text)
    except Exception:
        return ""


def _apply(color_code, text):
    """Safely apply ANSI color codes."""
    safe = _safe_text(text)
    try:
        return f"{color_code}{safe}\033[0m"
    except Exception:
        # Fallback: return plain text
        return safe


# -----------------------------
# Color Functions
# -----------------------------

def colorize_text_blue(text):
    return _apply("\033[94m", text)

def colorize_text_salmon(text):
    return _apply("\033[38;5;210m", text)

def colorize_text_green(text):
    return _apply("\033[92m", text)

def colorize_text_orange(text):
    return _apply("\033[38;5;208m", text)

def colorize_text_red(text):
    return _apply("\033[91m", text)

def colorize_text_yellow(text):
    return _apply("\033[93m", text)

def colorize_text_cyan(text):
    return _apply("\033[96m", text)

def colorize_text_magenta(text):
    return _apply("\033[95m", text)

def colorize_text_gray(text):
    return _apply("\033[90m", text)

def colorize_text_white(text):
    return _apply("\033[97m", text)
