"""
File: main.py
Author: YiHang
Created on: 01-10-2023
Last Modified: 01-10-2023
Description: matting-image based rembg
"""

from tkinter import Image
import rembg
from PIL import Image, ImageFilter
import numpy as np
import io
import os
import cairosvg
import warnings

from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


def add_icon_to_image(input_folder, output_folder, icon_path, icon_size_percentage=0.2, margin_percentage=0.1,
                      margin_top_percentage=0):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            # Construct full paths for input and output files
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"output_{filename}")

            # Read the input image
            with open(input_path, "rb") as input_file:
                input_data = input_file.read()
                output_data = rembg.remove(input_data)

            # Convert the output data to a PIL image
            with Image.open(io.BytesIO(output_data)) as img:
                # Create a solid color background, ensuring it has the same resolution as the original image
                background = Image.new("RGB", img.size, (0, 0, 0))  # Here, a black background is used; you can modify it as needed

                # Composite the image after matting onto the background
                result = Image.alpha_composite(background.convert("RGBA"), img.convert("RGBA"))

                # Calculate the new icon size
                new_icon_width = int(img.width * icon_size_percentage)
                new_icon_height = int(img.height * icon_size_percentage)

                # Calculate the top-left coordinates of the icon
                margin_left = int(img.width * margin_percentage)
                margin_top = int(img.height * margin_top_percentage)

                # Use cairosvg to render the SVG icon as an image
                svg_data = open(icon_path, "rb").read()
                icon = cairosvg.svg2png(svg_data, write_to=None, output_width=new_icon_width, output_height=new_icon_height,
                                        parent_width=img.width, parent_height=img.height)

                # Convert the SVG icon to a PIL image
                icon_img = Image.open(io.BytesIO(icon)).convert("RGBA")

                # Resize the result image to the original image's resolution
                result = result.resize(img.size, 3)

                # Paste the icon at the top-left corner
                result.paste(icon_img, (margin_left, margin_top), icon_img)

                # Save the resulting image
                result.save(output_path, "PNG")


# Specify the input folder, output folder, and SVG icon path
input_folder_path = "input_folder"
output_folder_path = "output_folder"
svg_icon_path = "logo1.svg"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Call the add_icon_to_image function
    add_icon_to_image(input_folder_path, output_folder_path, svg_icon_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/ change chinese to english
