import os
import shutil
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from PIL import Image
import io

def rotate_and_flip_image(image_data):
    """Rotate an image by 180 degrees and flip it horizontally."""
    image = Image.open(io.BytesIO(image_data))
    rotated_image = image.rotate(180)
    flipped_image = rotated_image.transpose(Image.FLIP_LEFT_RIGHT)
    byte_arr = io.BytesIO()
    flipped_image.save(byte_arr, format=image.format)
    return byte_arr.getvalue()

def remove_images_by_dimensions(book, target_dimensions):
    """Remove all images that match the specified dimensions."""
    items_to_remove = []  # Collect items to remove
    # Convert the generator to a list to allow modification
    items_list = list(book.get_items())
    
    for item in items_list:
        if item.get_type() == ebooklib.ITEM_IMAGE:
            # Get image data
            image_data = item.get_content()
            image = Image.open(io.BytesIO(image_data))
            width, height = image.size

            # Check if the image dimensions match any of the target dimensions
            if (width, height) in target_dimensions:
                print(f"Removing image: {item.get_name()} (Dimensions: {width}x{height})")
                items_to_remove.append(item)  # Add item to removal list
                
    # Remove items after iteration is complete
    for item in items_to_remove:
        items_list.remove(item)  # Remove item from the list
    
    # Update the book's items
    book.items = items_list
    
    return book

def main():
    # Get the filename from the user
    input_filename = input("Enter the filename: ")

    # Check if the file exists
    if not os.path.exists(input_filename):
        print(f"File '{input_filename}' does not exist.")
        return

    # Generate the new filename
    base, ext = os.path.splitext(input_filename)
    output_filename = f"{base}-clean{ext}"

    # Process the EPUB file
    if ext.lower() == '.epub':
        try:
            # Read the EPUB file
            book = epub.read_epub(input_filename)

            # Get the two sets of image dimensions to remove
            print("Enter the dimensions of the first set of images to remove:")
            width1 = int(input("Enter width of the first set: "))
            height1 = int(input("Enter height of the first set: "))

            print("Enter the dimensions of the second set of images to remove:")
            width2 = int(input("Enter width of the second set: "))
            height2 = int(input("Enter height of the second set: "))

            # Remove the images with the specified dimensions
            target_dimensions = [(width1, height1), (width2, height2)]
            book = remove_images_by_dimensions(book, target_dimensions)

            # Iterate through all items in the EPUB to modify text and rotate/flip images
            for item in book.get_items():
                # Process text/html items to replace the string
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse the content with BeautifulSoup
                    soup = BeautifulSoup(item.get_body_content(), 'html.parser')

                    # Replace all instances of "I l@ve RuBoard"
                    modified_content = soup.prettify().replace("I l@ve RuBoard", "")

                    # Update the item content
                    item.set_content(modified_content.encode('utf-8'))

                # Process image items to rotate and flip them (if not removed)
                elif item.get_type() == ebooklib.ITEM_IMAGE:
                    # Rotate and flip image
                    modified_image_data = rotate_and_flip_image(item.get_content())
                    item.set_content(modified_image_data)

            # Write the modified EPUB to a new file
            epub.write_epub(output_filename, book)
            print(f"Modified content and saved as '{output_filename}'")
        except Exception as e:
            print(f"Failed to process the EPUB file: {e}")
    else:
        print(f"Unsupported file extension '{ext}'. This script only supports EPUB files.")

if __name__ == "__main__":
    main()
