from PIL import Image
import rembg
import io
import os
import cairosvg


class ImageProcessor:
    def __init__(self, input_folder, output_folder, icon_path, background_image_path,
                 icon_size_percentage=0.3, margin_percentage=0.1, margin_top_percentage=0, crop_left_percentage=0.35):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.icon_path = icon_path
        self.background_image_path = background_image_path
        self.icon_size_percentage = icon_size_percentage
        self.margin_percentage = margin_percentage
        self.margin_top_percentage = margin_top_percentage
        self.crop_left_percentage = crop_left_percentage

    def process_images(self):
        # Ensure the output folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Get all files in the input folder
        for filename in os.listdir(self.input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg")):
                # Construct full paths for input and output files
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(self.output_folder, filename)

                # Read the input image using rembg to remove the background
                with open(input_path, "rb") as input_file:
                    input_data = input_file.read()
                    output_data = rembg.remove(input_data)

                # Convert the output data to a PIL image
                with Image.open(io.BytesIO(output_data)) as img:
                    # Crop the image by removing the left part
                    crop_left = int(img.width * self.crop_left_percentage)
                    crop_img = img.crop((crop_left, 0, img.width, img.height))

                    # Load the background image
                    background = Image.open(self.background_image_path).convert("RGBA")

                    # Create a new image with the size of the larger background image
                    new_canvas = Image.new("RGBA", background.size, (0, 0, 0, 0))

                    # Calculate the position to paste the cropped image at the center of the new canvas
                    paste_position = ((background.width - crop_img.width) // 2, (background.height - crop_img.height) // 2)

                    # Paste the cropped image onto the center of the new canvas
                    new_canvas.paste(crop_img, paste_position, crop_img)

                    # Composite the new canvas with the background
                    result = Image.alpha_composite(background, new_canvas)

                    # Calculate the new icon size
                    new_icon_width = int(crop_img.width * self.icon_size_percentage)
                    new_icon_height = int(crop_img.height * self.icon_size_percentage)

                    # Calculate the top-left coordinates of the icon
                    margin_left = int(crop_img.width * self.margin_percentage)
                    margin_top = int(crop_img.height * self.margin_top_percentage)

                    # Use cairosvg to render the SVG icon as an image
                    svg_data = open(self.icon_path, "rb").read()
                    icon = cairosvg.svg2png(svg_data, write_to=None, output_width=new_icon_width, output_height=new_icon_height,
                                            parent_width=crop_img.width, parent_height=crop_img.height)

                    # Convert the SVG icon to a PIL image
                    icon_img = Image.open(io.BytesIO(icon)).convert("RGBA")

                    # Paste the icon at the top-left corner
                    result.paste(icon_img, (margin_left, margin_top), icon_img)

                    # Save the resulting image
                    result.save(output_path, "PNG")


if __name__ == '__main__':
    # Specify input and output paths, SVG icon path, and background image path
    input_folder_path = "input_folder"
    output_folder_path = "output_folder"
    svg_icon_path = "logo1.svg"
    background_image_path = "background.png"

    # Create an instance of ImageProcessor
    processor = ImageProcessor(
        input_folder_path,
        output_folder_path,
        svg_icon_path,
        background_image_path,
        crop_left_percentage=0.35  # Adjust as needed
    )

    # Process the images
    processor.process_images()
