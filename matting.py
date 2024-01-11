from tkinter import Image
import rembg
from PIL import Image as PILImage
import numpy as np
import io
import os
import cairosvg


class ImageProcessor:
    def __init__(self, input_folder, output_folder, icon_path_black, icon_path_white,
                 icon_size_percentage=0.2, margin_percentage=0.1, margin_top_percentage=0):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.icon_path_black = icon_path_black
        self.icon_path_white = icon_path_white
        self.icon_size_percentage = icon_size_percentage
        self.margin_percentage = margin_percentage
        self.margin_top_percentage = margin_top_percentage

    def get_background_color(self, image):
        # Convert the image to a NumPy array
        img_array = np.array(image)

        # Calculate the mean color of the image
        mean_color = np.mean(img_array, axis=(0, 1))

        # Determine the background color based on the mean color
        if mean_color[0] >= 200 and mean_color[1] >= 200 and mean_color[2] >= 200:
            return "white"
        else:
            return "black"

    def add_icon_to_image(self, filename):
        input_path = os.path.join(self.input_folder, filename)
        output_path = os.path.join(self.output_folder, f"output_{filename}")

        with open(input_path, "rb") as input_file:
            input_data = input_file.read()
            output_data = rembg.remove(input_data)

        with PILImage.open(io.BytesIO(output_data)) as img:
            background_color = self.get_background_color(img)

            if background_color == "white":
                svg_icon_path = self.icon_path_black
                background = PILImage.new("RGBA", img.size, (255, 255, 255))
            else:
                svg_icon_path = self.icon_path_white
                background = PILImage.new("RGBA", img.size, (0, 0, 0))


            # Composite the image after matting onto the background
            result = PILImage.alpha_composite(background, img)

            new_icon_width = int(img.width * self.icon_size_percentage)
            new_icon_height = int(img.height * self.icon_size_percentage)

            margin_left = int(img.width * self.margin_percentage)
            margin_top = int(img.height * self.margin_top_percentage)

            svg_data = open(svg_icon_path, "rb").read()
            icon = cairosvg.svg2png(svg_data, write_to=None, output_width=new_icon_width,
                                    output_height=new_icon_height, parent_width=img.width, parent_height=img.height)

            icon_img = PILImage.open(io.BytesIO(icon)).convert("RGBA")

            result = result.resize(img.size, 3)
            result.paste(icon_img, (margin_left, margin_top), icon_img)

            # Save the resulting image
            result.save(output_path, "PNG")

    def process_images(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        for filename in os.listdir(self.input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                self.add_icon_to_image(filename)


if __name__ == '__main__':
    # Specify input and output paths, as well as SVG icon paths
    input_folder_path = "input_folder"
    output_folder_path = "output_folder"
    svg_icon_path_black = "logo.svg"
    svg_icon_path_white = "logo1.svg"

    # Create an instance of ImageProcessor and process the images
    processor = ImageProcessor(input_folder_path, output_folder_path, svg_icon_path_black, svg_icon_path_white)
    processor.process_images()
