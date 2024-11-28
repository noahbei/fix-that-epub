import os
import zipfile
from PIL import Image
from io import BytesIO
from ebooklib import epub
from lxml import etree

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size  # returns (width, height)

def process_image(image_data, rotate=True, flip=True):
    with Image.open(BytesIO(image_data)) as img:
        # Rotate and flip the image
        if rotate:
            img = img.rotate(180)
        if flip:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        
        # Save to a new byte array
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

def clean_epub(input_epub, dimension1, dimension2, output_epub):
    try:
        # Load the EPUB file
        book = epub.read_epub(input_epub)
        
        # Get the image files and their dimensions
        image_files = []
        for item in book.get_items():
            if item.get_type() == epub.ITEM_IMAGE:
                image_files.append(item)
        
        # Remove images by dimension
        for image in image_files:
            img_data = image.content
            img_width, img_height = get_image_dimensions(BytesIO(img_data))
            if (img_width == dimension1[0] and img_height == dimension1[1]) or \
               (img_width == dimension2[0] and img_height == dimension2[1]):
                # Remove the image from the EPUB
                book.get_items().remove(image)
                print(f"Removed image with dimensions: {img_width}x{img_height}")
        
        # Rotate and flip remaining images
        for image in book.get_items():
            if image.get_type() == epub.ITEM_IMAGE:
                img_data = image.content
                new_img_data = process_image(img_data)
                image.content = new_img_data
                print(f"Processed image: {image.get_name()}")
        
        # Save the cleaned EPUB to a new file
        book.save(output_epub)
        print(f"Cleaned EPUB saved to {output_epub}")
    
    except Exception as e:
        print(f"Error processing the EPUB: {e}")

def main():
    input_epub = input("Enter the path to the EPUB file: ")
    dimension1_width = int(input("Enter the width for the first image dimension to remove: "))
    dimension1_height = int(input("Enter the height for the first image dimension to remove: "))
    dimension2_width = int(input("Enter the width for the second image dimension to remove: "))
    dimension2_height = int(input("Enter the height for the second image dimension to remove: "))
    
    dimension1 = (dimension1_width, dimension1_height)
    dimension2 = (dimension2_width, dimension2_height)
    
    output_epub = os.path.splitext(input_epub)[0] + "-clean.epub"
    
    clean_epub(input_epub, dimension1, dimension2, output_epub)

if __name__ == "__main__":
    main()
