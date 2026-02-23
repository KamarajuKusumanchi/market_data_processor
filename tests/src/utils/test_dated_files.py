import os
import shutil
import tempfile

from src.utils.dated_files import find_files_with_date


def test_find_files_with_date():
    # Create a temporary directory for testing that will be automatically
    # cleaned up.
    temp_dir = tempfile.mkdtemp()

    try:
        # Define the files for the test
        dated_files = [
            "report_20231026.txt",
            "document_20230515_final.pdf",
            "log_20240101.csv",
            "20220228_backup.zip",
        ]
        non_dated_files = ["notes.md", "image.jpg", "plain_text.txt"]

        # Create the dummy files in the temporary directory
        for filename in dated_files + non_dated_files:
            with open(os.path.join(temp_dir, filename), 'w') as f:
                f.write("Test content.")

        # Call the function with the temporary directory path
        found_files = find_files_with_date(temp_dir)

        # Assert that the list of found files matches the expected list
        assert sorted(found_files) == sorted(dated_files)

    finally:
        # Clean up the temporary directory and its contents
        shutil.rmtree(temp_dir)
