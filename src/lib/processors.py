from find_system_fonts_filename import get_system_fonts_filename

from src.main import process_variable_fonts


def main():
    USER_FONTS = get_system_fonts_filename()
    USER_VARIABLE_FONTS = sorted(
        [user_font for user_font in USER_FONTS if user_font.lower().endswith(".ttf")]
    )
    process_variable_fonts(USER_VARIABLE_FONTS)
