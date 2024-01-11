from tkinter import PhotoImage
from PIL import Image, ImageFilter
import numpy as np
import io
import os
import cairosvg
import warnings

from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)


def get_background_color(image):
    # Convert the image to a NumPy array
    img_array = np.array(image)

    # Calculate the mean color of the image
    mean_color = np.mean(img_array, axis=(0, 1))

    # Determine the background color based on the mean color
    if mean_color[0] >= 200 and mean_color[1] >= 200 and mean_color[2] >= 200:
        return "white"
    else:
        return "black"


def add_icon_to_image(input_folder, output_folder, icon_path_black, icon_path_white, icon_size_percentage=0.2,
                      margin_percentage=0.1, margin_top_percentage=0):
    # Make sure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Gets all the files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            # Construct the input and output file's full path
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # Use the original image as a base
            with Image.open(input_path) as img:
                # Get the background color of the image
                background_color = get_background_color(img)

                # Choose the appropriate logo based on the background color
                if background_color == "white":
                    svg_icon_path = icon_path_black
                else:
                    svg_icon_path = icon_path_white

                # Calculate the new icon size
                new_icon_width = int(img.width * icon_size_percentage)
                new_icon_height = int(img.height * icon_size_percentage)

                # Computes the top-left coordinate of the icon
                margin_left = int(img.width * margin_percentage)
                margin_top = int(img.height * margin_top_percentage)

                # Use cairosvg to render SVG ICONS as images
                svg_data = open(svg_icon_path, "rb").read()
                icon = cairosvg.svg2png(svg_data, write_to=None, output_width=new_icon_width,
                                        output_height=new_icon_height,
                                        parent_width=img.width, parent_height=img.height)

                # Convert SVG icon to PIL image
                icon_img = Image.open(io.BytesIO(icon)).convert("RGBA")

                # Paste the icon in the top left corner
                img.paste(icon_img, (margin_left, margin_top), icon_img)

                # Save resulting image
                img.save(output_path, "PNG")


# Specify the input folder, output folder, and SVG icon paths for black and white backgrounds
input_folder_path = "input_folder"
output_folder_path = "output_folder"
svg_icon_path_black = "logo.svg"
svg_icon_path_white = "logo1.svg"

# Call the add_icon_to_image function with the specified paths
add_icon_to_image(input_folder_path, output_folder_path, svg_icon_path_black, svg_icon_path_white)
