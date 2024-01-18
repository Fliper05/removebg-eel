import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from rembg import remove
import io
import eel

print("Initializing Eel")
eel.init('web')  # Assuming 'web' is the directory that contains your web files

selected_directory = None  # Global variable

@eel.expose
def select_directory(directory=None):
    global selected_directory  # Declare that we want to use the global variable
    if directory is not None:
        print(f"Selected folder: {directory}")
        eel.updateSelectedFolder(directory)  # Update the selected folder in HTML
        selected_directory = directory  # Update the global variable
    return selected_directory

@eel.expose
def copy_and_rename_folder():
    global selected_directory
    print(f"Copying and renaming folder: {selected_directory}")
    dst_folder = selected_directory + '_bilepozadi'
    os.makedirs(dst_folder, exist_ok=True)
    return dst_folder


def remove_background(image_path):
    print(f"Removing background from image: {image_path}")
    with open(image_path, 'rb') as img_file:
        img = img_file.read()
    img_no_bg = remove(img)
    img_no_bg = Image.open(io.BytesIO(img_no_bg))

    # Create a new image with a white background
    white_bg = Image.new('RGBA', img_no_bg.size, 'white')
    white_bg.paste(img_no_bg, (0, 0), img_no_bg)

    return white_bg.convert('RGB')  # Convert to RGB if saving as JPEG

def save_image(image, save_path):
    print(f"Saving image to: {save_path}")
    rgb_image = image.convert('RGB')
    rgb_image.save(save_path)


@eel.expose
def remove_background_all_images():
    global selected_directory
    print("Removing background from all images")
    result = {"status": "", "message": ""}
    try:
        src_folder = select_directory()
        dst_folder = copy_and_rename_folder()
        result["status"] = "Úspěch"
        result["message"] = f"Vybraná složka {src_folder}\nNová složka {dst_folder}"

        total_files = sum([len(files) for r, d, files in os.walk(src_folder)])
        processed_files = 0

        for dirpath, dirnames, filenames in os.walk(src_folder):
            for dirname in dirnames:
                src_dir = os.path.join(dirpath, dirname)
                relative_dirpath = os.path.relpath(src_dir, src_folder)
                dst_dir = os.path.join(dst_folder, relative_dirpath)
                os.makedirs(dst_dir, exist_ok=True)
            for filename in filenames:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                    image_path = os.path.join(dirpath, filename)
                    relative_dirpath = os.path.relpath(dirpath, src_folder)
                    save_dirpath = os.path.join(dst_folder, relative_dirpath)
                    os.makedirs(save_dirpath, exist_ok=True)  # Create directory for the file
                    save_path = os.path.join(save_dirpath, filename)
                    if save_path.lower().endswith(('.jpg', '.jpeg')):
                        save_path = save_path.rsplit('.', 1)[0] + '.png'
                    image_without_background = remove_background(image_path)
                    save_image(image_without_background, save_path)
                processed_files += 1
                eel.updateProgress(processed_files / total_files * 100)  # Update the progress bar

        result["message"] += f"\nOdbělených souborů ve složce {src_folder}: {processed_files}"
    except Exception as e:
        result["status"] = "Chyba"
        result["message"] = f"Došlo k chybě {str(e)}"

    eel.updateStatusMessage(result["status"], result["message"])  # Update the status message in HTML




if __name__ == '__main__':
    print("Starting Eel")
    eel.start('index.html')  # Use your actual HTML file name

    