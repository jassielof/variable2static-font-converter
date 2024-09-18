# Variable Font to Static Font Converter

This Python script automates the process of converting variable fonts (.ttf) to multiple static font instances. It's designed to process all variable fonts in a specified directory, creating static instances for predefined or custom weight values.

## Features

- Converts variable fonts to static instances
- Supports batch processing of multiple fonts
- Configurable weight values via JSON file
- Command-line arguments for specifying input and output directories
- Parallel processing for improved performance
- Progress bar for visual feedback
- Detailed logging

## Requirements

- Python 3.6+
- fonttools
- tqdm

## Installation

1. Clone this repository or download the script.
2. Install the required packages:

```bash
pip install fonttools tqdm
```

## Usage

1. Place your variable font files (.ttf) in the input directory.

2. (Optional) Create a `config.json` file in the same directory as the script to specify custom weights:

```json
{
  "weights": {
    "Thin": 100,
    "Regular": 400,
    "Bold": 700
  }
}
```

3. Run the script:

```bash
python font_converter.py --input /path/to/input/fonts --output /path/to/output
```

Or use default paths:

```bash
python font_converter.py
```

## Output

The script will create an output directory structure as follows:

```
output/
├── Font1/
│   ├── Font1-Thin.ttf
│   ├── Font1-Regular.ttf
│   └── Font1-Bold.ttf
├── Font2/
│   ├── Font2-Thin.ttf
│   ├── Font2-Regular.ttf
│   └── Font2-Bold.ttf
...
```

## Logging

The script generates a `font_conversion.log` file with detailed information about the conversion process.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/font-converter/issues) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
