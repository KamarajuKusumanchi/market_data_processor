import os
import re


def find_files_with_date(directory_path):
    """
    Finds all files in a directory that have a YYYYMMDD date in their filename.

    Args:
        directory_path (str): The path to the directory to search.

    Returns:
        list: A list of filenames that contain a date.
    """
    # Regex pattern to match YYYYMMDD format in the filename
    # \d{4} matches 4 digits for the year
    # \d{2} matches 2 digits for the month
    # \d{2} matches 2 digits for the day
    date_pattern = re.compile(r'\d{4}\d{2}\d{2}')

    found_files = []

    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return found_files

    # Iterate through all entries in the directory
    for filename in os.listdir(directory_path):
        # Check if the filename matches the date pattern
        if date_pattern.search(filename):
            found_files.append(filename)

    return found_files
