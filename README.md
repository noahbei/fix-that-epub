# EPUB Cleaner Script
This repository contains a script to clean up an EPUB file by fixing various issues such as upside-down images, watermarks, unwanted navigation links/buttons, and improperly flowing text. The script is designed to be used from the command line, reading an input EPUB file and generating a cleaned version with "-clean" appended to the filename.
All code is written by AI to test the extent of its ability. No human modifications have been made.

## Features
- Rotate upside-down images to the correct orientation
- Remove watermark (RUBoard)
- Remove unnecessary next/prev navigation links/buttons
## Requirements
- Python 3.x
- `os` module
- `shutil` module
- `ebooklib` module
- `bs4` module (BeautifulSoup)
- `PIL` module (Pillow)
- `io` module

## Usage
1. Clone this repository or download the script.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the script.
4. Run the script with the following command:
   ```sh
   python epub_cleaner.py <input_file.epub>
   ```
This will generate a cleaned EPUB file with "-clean" appended to the original filename.

## How It Works
The script extracts the EPUB file (which is a ZIP archive) to a temporary directory.
It processes each file within the EPUB:
Fixes image orientation using the Pillow library.
Removes watermarks and unnecessary navigation links/buttons by parsing and modifying the HTML/XML content.
The modified files are then zipped back into a new EPUB file with "-clean" appended to the original filename.
Example
  ```sh
  python epub_cleaner.py ThePragmaticProgrammer.epub
  ```
This will produce a cleaned EPUB file named ThePragmaticProgrammer-clean.epub.

## Notes
Ensure you have the necessary permissions to read and write files in the directory where you run the script.
This script was generated using AI tools like ChatGPT and GitHub Copilot. It may require minor adjustments based on specific EPUB file structures.

## Acknowledgements
This script was generated with the help of AI tools such as ChatGPT and GitHub Copilot. Special thanks to the developers of these tools for making this project possible.
