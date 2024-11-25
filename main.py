import os
import shutil
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

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

            # Iterate through all items in the EPUB
            for item in book.get_items():
                # Only process text/html items
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse the content with BeautifulSoup
                    soup = BeautifulSoup(item.get_body_content(), 'html.parser')

                    # Replace all instances of "I l@ve RuBoard"
                    modified_content = soup.prettify().replace("I l@ve RuBoard", "")

                    # Update the item content
                    item.set_content(modified_content.encode('utf-8'))

            # Write the modified EPUB to a new file
            epub.write_epub(output_filename, book)
            print(f"Modified content and saved as '{output_filename}'")
        except Exception as e:
            print(f"Failed to process the EPUB file: {e}")
    else:
        print(f"Unsupported file extension '{ext}'. This script only supports EPUB files.")

if __name__ == "__main__":
    main()
