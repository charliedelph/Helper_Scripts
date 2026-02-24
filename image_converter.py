import os
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm  # Library for the visual progress bar

# This allows the Pillow library to "understand" HEIC files from iPhones
register_heif_opener()

# --- GLOBAL SETTINGS ---
# 1. Update the source directory folder containing your images 
SOURCE_DIRECTORY = r"FILE_PATH_TO_FOLDER_OF_FILES_TO_CONVERT" # <--- Update the text in the quotes
# 2. Choose Input and Output Formats
# Common choices: .heic, .jpg, .png, .webp, .bmp, .tiff
FROM_EXT = ".heic"
TO_EXT   = ".jpg"

# 3. Image Quality (1-100) - Only affects JPG and WEBP
QUALITY = 95
# -----------------------

def universal_convert(folder_path, ext_from, ext_to):
    """
    Scans a folder and converts images between any formats supported by Pillow.
    """
    # Clean up dots in extensions
    ext_from = "." + ext_from.lstrip('.')
    ext_to = "." + ext_to.lstrip('.')

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return

    # Create output folder
    output_folder_name = ext_to.replace(".", "").upper()
    output_folder = os.path.join(folder_path, output_folder_name)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get list of matching files
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(ext_from.lower())]
    
    if not files:
        print(f"No files found with extension {ext_from} in {folder_path}")
        return

    print(f"Found {len(files)} files. Converting {ext_from} -> {ext_to}...")

    count = 0
    for filename in files:
        try:
            full_path = os.path.join(folder_path, filename)
            clean_name = os.path.splitext(filename)[0]
            save_path = os.path.join(output_folder, f"{clean_name}{ext_to}")

            with Image.open(full_path) as img:
                # HANDLE TRANSPARENCY: 
                # If converting to JPG, we must remove transparency (Alpha channel)
                if ext_to.lower() in [".jpg", ".jpeg"]:
                    if img.mode in ("RGBA", "P", "LA"):
                        # Create a white background and paste the image over it
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                        img = background
                    else:
                        img = img.convert("RGB")

                # Save the image
                img.save(save_path, quality=QUALITY, subsampling=0)
                count += 1
                print(f"[{count}] Processed: {filename}")

        except Exception as e:
            print(f"Skipped {filename} due to error: {e}")

    print(f"\nSuccess! {count} files saved to: {output_folder}")

if __name__ == "__main__":
    universal_convert(SOURCE_DIRECTORY, FROM_EXT, TO_EXT)
