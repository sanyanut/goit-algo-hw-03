import os
import shutil
import argparse


def parse_args():
    try:
        parser = argparse.ArgumentParser(
            description="Sort and copy files to folders by extention"
        )
        parser.add_argument("input_dir", help="Path to the source directory")
        parser.add_argument(
            "output_dir",
            nargs="?",
            default="dist",
            help="Path to the distdirectory",
        )
        return parser.parse_args()
    except Exception as e:
        print(e)


def process_directory(source_path, dist_path):
    try:
        for item in os.listdir(source_path):
            item_path = os.path.join(source_path, item)

            if os.path.isdir(item_path):
                # Recursive call for subdirectories
                process_directory(item_path, dist_path)
            elif os.path.isfile(item_path):
                # Process file for copying
                copy_file(item_path, dist_path)
    except OSError as e:
        print(f"OS error accessing directory {source_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in directory {source_path}: {e}")


def copy_file(file_path, dist_path):
    try:
        _, file_extension = os.path.splitext(file_path)
        extension_dir_name = (
            file_extension[1:] if file_extension else "no_extension_directory"
        )

        destination_subdir = os.path.join(dist_path, extension_dir_name)
        os.makedirs(destination_subdir, exist_ok=True)

        dist_file_path = os.path.join(destination_subdir, os.path.basename(file_path))

        shutil.copy2(file_path, dist_file_path)
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except shutil.Error as e:
        print(f"Copying error for '{file_path}': {e}")
    except Exception as e:
        print(f"An unexpected error for '{file_path}': {e}")


def main():
    args = parse_args()
    source_directory = args.input_dir
    destination_directory = args.output_dir

    # Create destination directory if it doesn't exist
    try:
        os.makedirs(destination_directory, exist_ok=True)
        print(
            f"Processing files from '{source_directory}' to '{destination_directory}'..."
        )
        process_directory(source_directory, destination_directory)
    except Exception as e:
        print(f"Failed to create destination directory: {e}")


if __name__ == "__main__":
    main()
