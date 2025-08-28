from datetime import datetime
import os
import logging
from find_system_fonts_filename import get_system_fonts_filename
from fontTools import ttLib
from fontTools.varLib import instancer

from lib.weights import WEIGHTS


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


def update_font_names(font, weight_name):
    # Update name table entries
    for name in font["name"].names:
        if name.nameID in (
            1,
            3,
            4,
            6,
        ):  # Family name, Unique identifier, Full name, PostScript name
            current_name = name.toUnicode()
            if name.nameID in (1, 3, 4):
                new_name = f"{current_name} {weight_name}"
            else:  # PostScript name
                new_name = f"{current_name.replace(' ', '')}-{weight_name}"
            name.string = new_name.encode(name.getEncoding())


def create_static_fonts(selected_fonts):
    overwrite_mode = None
    for font_number, input_font in selected_fonts:
        try:
            font = ttLib.TTFont(input_font)
            if "fvar" not in font:
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

            if (
                existing_fonts
                and overwrite_mode != "all"
                and overwrite_mode != "skip_all"
            ):
                print(f"\nFont: {os.path.basename(input_font)}")
                print("The following static fonts already exist:")
                for weight_name, existing_path in existing_fonts:
                    print(f"- {os.path.basename(existing_path)}")

                while True:
                    choice = (
                        input(
                            "\nChoose action:\n"
                            "Overwrite existing fonts: 'o'\n"
                            "Skip this font: s\n"
                            "Overwrite all existing fonts (for this and following): O\n"
                            "Skip all existing fonts (for this and following): S\n"
                            "Cancel operation: c\n"
                            "Choice: "
                        )
                        .lower()
                        .strip()
                    )

                    if choice == "o":
                        break
                    elif choice == "s":
                        fonts_to_create = [
                            (w, v, p)
                            for w, v, p in fonts_to_create
                            if not os.path.exists(p)
                        ]
                        break
                    elif choice == "O":
                        overwrite_mode = "all"
                        break
                    elif choice == "S":
                        overwrite_mode = "skip_all"
                        fonts_to_create = [
                            (w, v, p)
                            for w, v, p in fonts_to_create
                            if not os.path.exists(p)
                        ]
                        break
                    elif choice == "c":
                        return
                    else:
                        print("Invalid choice")
            elif existing_fonts and overwrite_mode == "skip_all":
                fonts_to_create = [
                    (w, v, p) for w, v, p in fonts_to_create if not os.path.exists(p)
                ]
            if not fonts_to_create:
                print(f"No new fonts to create for {os.path.basename(input_font)}")
                continue
            for weight_name, weight_value, output_path in fonts_to_create:
                try:
                    static_font = instancer.instantiateVariableFont(
                        font, {"wght": weight_value}
                    )
                    update_font_names(static_font, weight_name)
                    static_font.save(output_path)
                except Exception as e:
                    logging.error(
                        f"Failed to create static font for weight {weight_name} of {os.path.basename(input_font)}: {str(e)}"
                    )
            logging.info(
                f"Font conversion completed successfully for {os.path.basename(input_font)}"
            )
        except Exception as e:
            logging.error(
                f"An error occurred during font conversion for {os.path.basename(input_font)}: {str(e)}"
            )


def process_variable_fonts(variable_fonts):
    counter = 0
    numbered_fonts = {}

    for variable_font in variable_fonts:
        counter += 1
        print(f"{counter}. {os.path.basename(variable_font)}")
        numbered_fonts[counter] = variable_font

    print(
        "\nSelect a single, or range of fonts...\n"
        "- For a single font: n\n"
        "- For a range of fonts: n-m\n"
        "- For multiple single or range of fonts (space after comma is valid): n, m-p, ...\n"
    )

    user_input = input(f"Fonts (1-{counter}): ")
    normalized_inputs = []

    try:
        parts = user_input.replace(" ", "").split(",")
        for part in parts:
            if "-" in part:
                start, end = map(int, part.split("-"))
                if start > end:
                    start, end = end, start
                normalized_inputs.extend(range(start, end + 1))
            else:
                normalized_inputs.append(int(part))
        normalized_inputs = sorted(set(normalized_inputs))
        print(f"\nProcessing fonts: {normalized_inputs}\n")
    except ValueError:
        print("Invalid input. Please enter valid font selections.")
        return

    selected_fonts = sorted(
        [(i, numbered_fonts[i]) for i in normalized_inputs if i in numbered_fonts]
    )

    print("Selected fonts:")
    for number, selected_font in selected_fonts:
        print(f"{number}. {os.path.basename(selected_font)}")

    user_input = input("\nContinue? (enter to confirm)")
    if user_input != "":
        return

    create_static_fonts(selected_fonts)
