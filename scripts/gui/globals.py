#colour palette
primary_colour = "#000000"
secondary_colour = "#000000"
bg_colour = "#000000"
text_div_colour = "#000000"
text_high_contrast = "#000000"
is_dark = False

def light_mode():
    global primary_colour, secondary_colour, bg_colour, text_div_colour, text_high_contrast, is_dark
    primary_colour = "#0B1F3B"
    secondary_colour = "#1F6AE1"
    bg_colour = "#CBCDCF"
    text_div_colour = "#ffffff"
    text_high_contrast = "#000000"
    is_dark = False

def dark_mode():
    global primary_colour, secondary_colour, bg_colour, text_div_colour, text_high_contrast, is_dark
    primary_colour = "#000000"
    secondary_colour = "#0B1F3B"
    bg_colour = "#1A1A1A"
    text_div_colour = "#ffffff"
    text_high_contrast = "#999999"
    is_dark = True