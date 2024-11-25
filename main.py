import os
import shutil

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

    # Copy the file to the new filename
    try:
        shutil.copy(input_filename, output_filename)
        print(f"Copied '{input_filename}' to '{output_filename}'")
    except Exception as e:
        print(f"Failed to copy file: {e}")

if __name__ == "__main__":
    main()
