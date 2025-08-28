import os


def select_fonts(variable_fonts):
    """
    Displays a list of fonts and prompts the user to select which ones to process.
    Handles parsing of single numbers, ranges, and comma-separated lists.
    """
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
        return None

    selected_fonts = sorted(
        [(i, numbered_fonts[i]) for i in normalized_inputs if i in numbered_fonts]
    )

    if not selected_fonts:
        print("No valid fonts selected.")
        return None

    print("Selected fonts:")
    for number, selected_font in selected_fonts:
        print(f"{number}. {os.path.basename(selected_font)}")

    user_input = input("\nContinue? (enter to confirm)")
    if user_input != "":
        return None

    return selected_fonts


def get_overwrite_choice(font_basename, existing_fonts):
    """
    Prompts the user on how to handle existing static fonts.
    """
    print(f"\nFont: {font_basename}")
    print("The following static fonts already exist:")
    for weight_name, existing_path in existing_fonts:
        print(f"- {os.path.basename(existing_path)}")

    while True:
        choice = (
            input(
                "\nChoose action:\n"
                "- 'o': Overwrite existing fonts\n"
                "- 's': Skip this font\n"
                "- 'O': Overwrite all existing fonts (for this and following)\n"
                "- 'S': Skip all existing fonts (for this and following)\n"
                "- 'c': Cancel operation\n"
                "\nChoice: "
            )
            .lower()
            .strip()
        )
        if choice in ("o", "s", "O", "S", "c"):
            return choice
        else:
            print("Invalid choice")
