from colored import fg, bg, attr


def colorize_text_blue(text_to_colorize) -> str:
    return f"{fg(12)}{text_to_colorize}{attr(0)}"


def colorize_text_red(text_to_colorize) -> str:
    return f"{fg(1)}{text_to_colorize}{attr(0)}"


def colorize_text_green(text_to_colorize) -> str:
    return f"{fg(10)}{text_to_colorize}{attr(0)}"


def colorize_text_salmon(text_to_colorize) -> str:
    return f"{fg(137)}{text_to_colorize}{attr(0)}"


def colorize_text_orange(text_to_colorize) -> str:
    return f"{fg(214)}{text_to_colorize}{attr(0)}"


def colorize_location_status(text_to_colorize) -> str:
    if "UNLOCATED" in text_to_colorize:
        return colorize_text_red(text_to_colorize)
    else:
        return colorize_text_orange(text_to_colorize)
