# Variable Font to Static Font Converter

This Python script automates the process of converting variable fonts (.ttf) to multiple static font instances. It's designed to process all variable fonts in a specified directory, creating static instances for predefined or custom weight values.

## Key Features

- **Automatic Font Processing**: Place your variable font files (.ttf) in the `myenv/fonts/` folder, and the script will automatically detect and process them.
- **Intelligent Output**: The script creates an output folder for each processed font, naming it after the original font file.
- **Batch Processing**: Converts multiple variable fonts in a single run.
- **Customizable Weights**: Define custom weight values via a configuration file.

## How It Works

1. **Input**: Place your variable font files (.ttf) in the `myenv/fonts/` directory.
2. **Processing**: Run the script. It automatically detects and processes all .ttf files in the input directory.
3. **Output**: For each input font, the script creates a dedicated output folder named after the font. Inside this folder, you'll find the generated static font instances.

## Usage

1. Ensure you have Python and the required dependencies installed.
2. Place your variable font files in the `myenv/fonts/` directory.
3. Run the script:
   ```
   python src/scripts/variable_to_static_font_converter.py
   ```
4. Check the `myenv/fonts/output/` directory for your converted fonts. Each font will have its own subfolder.

## Example

If you place `MyFont-Variable.ttf` in the `myenv/fonts/` directory and run the script, you'll find the output in `myenv/fonts/output/MyFont-Variable/`, containing files like:
- `MyFont-Variable-Thin.ttf`
- `MyFont-Variable-Regular.ttf`
- `MyFont-Variable-Bold.ttf`
(Exact output files depend on the weight configurations)

## Configuration

You can customize the weight values by modifying the `config.json` file in the script's directory.

## Requirements

- Python 3.6+
- fonttools
- (Any other dependencies your script uses)

## Installation

(Include installation instructions here)

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/font-converter/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)