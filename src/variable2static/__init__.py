import logging
from find_system_fonts_filename import get_system_fonts_filename

from datetime import datetime
import os
from fontTools import ttLib

from lib.weights import WEIGHTS
from lib.ui import select_fonts, get_overwrite_choice
from lib.processors import create_static_font_instance


LOGS_DIR = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__),
    ),
    "..",
    "..",
    "logs",
)
os.makedirs(LOGS_DIR, exist_ok=True)

# Create timestamp-based log filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"font_conversion_{timestamp}.log"


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, log_filename)),
        logging.StreamHandler(),
    ],
)


def create_static_fonts(selected_fonts):
    overwrite_mode = None  # Can be None, 'all', 'skip_all'
    for font_number, input_font in selected_fonts:
        try:
            font = ttLib.TTFont(input_font)
            if "fvar" not in font:
                logging.warning(
                    f"Skipping non-variable font: {os.path.basename(input_font)}"
                )
                continue

            font_dir = os.path.dirname(input_font)
            font_basename = os.path.splitext(os.path.basename(input_font))[0]

            fonts_to_create = []
            existing_fonts = []
            for weight_name, weight_value in WEIGHTS.items():
                output_path = os.path.join(
                    font_dir, f"{font_basename}-{weight_name}.ttf"
                )
                fonts_to_create.append((weight_name, weight_value, output_path))
                if os.path.exists(output_path):
                    existing_fonts.append((weight_name, output_path))

            if existing_fonts and overwrite_mode not in ("all", "skip_all"):
                choice = get_overwrite_choice(
                    os.path.basename(input_font), existing_fonts
                )
                if choice == "o":
                    pass  # Overwrite this time
                elif choice == "s":
                    fonts_to_create = [
                        (w, v, p)
                        for w, v, p in fonts_to_create
                        if not os.path.exists(p)
                    ]
                elif choice == "O":
                    overwrite_mode = "all"
                elif choice == "S":
                    overwrite_mode = "skip_all"
                    fonts_to_create = [
                        (w, v, p)
                        for w, v, p in fonts_to_create
                        if not os.path.exists(p)
                    ]
                elif choice == "c":
                    logging.info("Operation cancelled by user.")
                    return

            if overwrite_mode == "skip_all":
                fonts_to_create = [
                    (w, v, p) for w, v, p in fonts_to_create if not os.path.exists(p)
                ]

            if not fonts_to_create:
                logging.info(
                    f"No new fonts to create for {os.path.basename(input_font)}"
                )
                continue

            for weight_name, weight_value, output_path in fonts_to_create:
                create_static_font_instance(
                    font, weight_value, weight_name, output_path
                )

            logging.info(
                f"Font conversion completed for {os.path.basename(input_font)}"
            )

        except Exception as e:
            logging.error(
                f"An error occurred during font conversion for {os.path.basename(input_font)}: {str(e)}"
            )


def main() -> None:
    USER_VARIABLE_FONTS = sorted(
        [
            user_font
            for user_font in get_system_fonts_filename()
            if user_font.lower().endswith(".ttf")
        ]
    )

    if not USER_VARIABLE_FONTS:
        logging.info("No variable fonts found.")
        return

    SELECTED_FONTS = select_fonts(USER_VARIABLE_FONTS)

    if not SELECTED_FONTS:
        logging.info("No fonts selected. Exiting.")
        return

    create_static_fonts(SELECTED_FONTS)
    logging.info("Font conversion process completed.Remember to reset your font cache.")
