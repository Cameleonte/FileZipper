import os
import zipfile


def get_file_sizes(path):
        # Get the compressed size using zipfile
    with zipfile.ZipFile(path, 'r') as zip_file:
        new_compressed_size = sum(entry.compress_size for entry in zip_file.infolist() if not entry.is_dir())

    return new_compressed_size


def delete_old_zip(zip_name):
    """
    Delete the zip file if it already exists.

    :param zip_name: Name of the zip file to be deleted.
    """
    if os.path.exists(zip_name):
        os.remove(zip_name)
        print(f"Deleted old {zip_name}")
    else:
        print(f"{zip_name} does not exist, skipping delete.")


def zip_current_level(exclude_list, zip_name="output.zip"):
    """
    Zip every folder and file at the current level.

    :param exclude_list: List of folders and files to be excluded.
    :param zip_name: Name of the resulting zip file.
    """

    # Delete old zip if it exists
    delete_old_zip(zip_name)

    # Get all folders and files in the current directory
    items = os.listdir()

    # Remove items from the exclude_list
    items_to_zip = [item for item in items if item not in exclude_list]

    # Create a zip archive
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for item in items_to_zip:
            if os.path.isfile(item):
                zipf.write(item)
            elif os.path.isdir(item):
                for dirpath, dirnames, filenames in os.walk(item):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        arcname = os.path.relpath(file_path, start='.')
                        zipf.write(file_path, arcname=arcname)


if __name__ == "__main__":
    # List of folders and files to be excluded
    exclude_list = ["venv", ".idea", "templates", "file_zipper.py", "populate_db.py"]

    zip_current_level(exclude_list)

    file_path = 'output.zip'
    compressed_size = get_file_sizes(file_path)

    print(f"Files and folders zipped into 'output.zip' excluding {exclude_list}\n")
    print(f'Compressed File Size: {compressed_size} bytes')
