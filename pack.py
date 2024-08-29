import os
import shutil

def count_files(directory):
    """ Count all files in the directory including subdirectories. """
    total = 0
    for root, dirs, files in os.walk(directory):
        total += len(files)
    return total

def copy_with_progress(src, dst, progress_callback):
    """ Copy files from src to dst with progress reporting using a callback function. """
    if os.path.isdir(src):
        files = os.listdir(src)
        total_files = count_files(src)
        copied_files = 0
        os.makedirs(dst, exist_ok=True)
        for item in files:
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copied_files += copy_with_progress(s, d, progress_callback)
            else:
                shutil.copy2(s, d)
                copied_files += 1
                progress_callback(copied_files, total_files, f"Copying: {s} to {d}")
        return copied_files
    else:
        shutil.copy2(src, dst)
        progress_callback(1, 1, f"Copying: {src} to {dst}")
        return 1

def pack(content_folder_location, db_file_location, module_folder_locations, output_dir, pack_name, progress_callback):
    # Create the pack directory structure
    pack_path = os.path.join(output_dir, pack_name)
    os.makedirs(pack_path, exist_ok=True)
    db_path = os.path.join(pack_path, 'db')
    content_path = os.path.join(pack_path, 'content')
    modules_path = os.path.join(pack_path, 'modules')
    os.makedirs(db_path, exist_ok=True)
    os.makedirs(content_path, exist_ok=True)
    os.makedirs(modules_path, exist_ok=True)

    # Copy database file
    copy_with_progress(db_file_location, os.path.join(db_path, 'solarspell_test.db'), progress_callback)

    # Copy content
    if os.path.isdir(content_folder_location):
        copy_with_progress(content_folder_location, content_path, progress_callback)

    # Copy modules
    for module_folder in module_folder_locations:
        if os.path.isdir(module_folder):
            destination_folder = os.path.join(modules_path, os.path.basename(module_folder))
            copy_with_progress(module_folder, destination_folder, progress_callback)

    # Rename the output directory
    packed_folder_path = pack_path + ".pack"
    os.rename(pack_path, packed_folder_path)
    progress_callback(None, None, f"Pack created at: {packed_folder_path}")

# Example usage
def progress_update(copied_files, total_files, message):
    if copied_files is not None and total_files is not None:
        print(f"{copied_files}/{total_files}: {message}")
    else:
        print(message)

if __name__ == "__main__":
    content_folder = "./content"
    db_file = "./your_database.db"
    modules_folders = ["./module1", "./module2"]
    output_directory = "./"
    pack_name = "test1"

    pack(content_folder, db_file, modules_folders, output_directory, pack_name, progress_update)
