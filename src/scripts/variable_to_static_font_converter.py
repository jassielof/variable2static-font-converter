import os
import sys
import logging
from fontTools import ttLib
from fontTools.varLib import instancer

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("font_conversion.log"),
                        logging.StreamHandler()
                    ])

def update_font_names(font, weight_name):
    # Update name table entries
    for name in font['name'].names:
        if name.nameID in (1, 3, 4, 6):  # Family name, Unique identifier, Full name, PostScript name
            current_name = name.toUnicode()
            if name.nameID in (1, 3, 4):
                new_name = f"{current_name} {weight_name}"
            else:  # PostScript name
                new_name = f"{current_name.replace(' ', '')}-{weight_name}"
            name.string = new_name.encode(name.getEncoding())

def create_static_fonts(input_font, output_dir, weights):
    try:
        # Load the variable font
        font = ttLib.TTFont(input_font)
        logging.info(f"Loaded variable font: {input_font}")
        
        # Create static instances for each specified weight
        for weight_name, weight_value in weights.items():
            output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(input_font))[0]}-{weight_name}.ttf")
            
            try:
                # Create a new instance with the specified weight
                static_font = instancer.instantiateVariableFont(font, {"wght": weight_value})
                
                # Update the font names
                update_font_names(static_font, weight_name)
                
                # Save the new static font
                static_font.save(output_path)
                logging.info(f"Created static font: {os.path.abspath(output_path)}")
            except Exception as e:
                logging.error(f"Failed to create static font for weight {weight_name}: {str(e)}")
        
        logging.info(f"Font conversion completed successfully for {input_font}")
    except Exception as e:
        logging.error(f"An error occurred during font conversion for {input_font}: {str(e)}")

def process_fonts_in_directory(font_dir):
    # Define the weights you want to generate with their conventional values
    weights = {
        "Thin": 100,
        "ExtraLight": 200,
        "Light": 300,
        "Regular": 400,
        "Medium": 500,
        "SemiBold": 600,
        "Bold": 700,
        "ExtraBold": 800,
        "Black": 900
    }
    
    # Process each .ttf file in the directory
    for filename in os.listdir(font_dir):
        if filename.lower().endswith('.ttf'):
            input_font = os.path.join(font_dir, filename)
            output_dir = os.path.join(font_dir, 'output', os.path.splitext(filename)[0])
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            create_static_fonts(input_font, output_dir, weights)

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the font folder in the virtual environment
    venv_font_dir = os.path.join(script_dir, '..', '..', 'myenv', 'fonts')
    
    # Check if the font directory exists
    if not os.path.exists(venv_font_dir):
        logging.error(f"Font directory not found: {venv_font_dir}")
        sys.exit(1)
    
    logging.info(f"Processing fonts in directory: {venv_font_dir}")
    process_fonts_in_directory(venv_font_dir)
    logging.info("All font conversions completed")