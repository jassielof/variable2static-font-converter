import os
import logging
from fontTools.varLib import instancer


def update_font_names(font, weight_name):
    """
    Updates the name table of a font to reflect its new weight.
    """
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


def create_static_font_instance(variable_font, weight_value, weight_name, output_path):
    """
    Creates a single static font instance for a given weight.
    """
    try:
        static_font = instancer.instantiateVariableFont(
            variable_font, {"wght": weight_value}
        )
        update_font_names(static_font, weight_name)
        static_font.save(output_path)
        logging.info(f"Successfully created {os.path.basename(output_path)}")
    except Exception as e:
        logging.error(
            f"Failed to create static font for weight {weight_name} from {variable_font.reader.file.name}: {str(e)}"
        )
