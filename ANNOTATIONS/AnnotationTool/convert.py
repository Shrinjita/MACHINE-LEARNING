import os
import argparse
from PIL import Image
import piexif

def convert_heic_to_jpg(heic_path, jpg_path):
    try:
        # Open the HEIC image using PIL
        heic_image = Image.open(heic_path)

        # Save the image in JPG format
        heic_image.save(jpg_path, "JPEG", quality=95)

        print(f"Conversion successful: {heic_path} -> {jpg_path}")
    except Exception as e:
        print(f"Conversion failed: {heic_path} -> {jpg_path}\nError: {e}")

def batch_convert(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(directory, filename)
            jpg_filename = filename.replace(".heic", ".jpg")
            jpg_path = os.path.join(output_directory, jpg_filename)
            convert_heic_to_jpg(heic_path, jpg_path)

def main():
    parser = argparse.ArgumentParser(description="Convert HEIC images to JPG format")
    parser.add_argument("input_directory", help=r"C:\\Users\\Shrinjita Paul\\Documents\\GitHub\\ImgCap\\ANNOTATIONS\\AnnotationTool\\img_new")
    parser.add_argument("output_directory", help=r"C:\\Users\\Shrinjita Paul\\Documents\\GitHub\\ImgCap\\ANNOTATIONS\\sp7112\\jpg")
    args = parser.parse_args()

    batch_convert(args.input_directory, args.output_directory)

if __name__ == "__main__":
    main()
 