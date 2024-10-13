# Duplicate File Remover

This Python program provides a simple graphical interface (GUI) to find and remove duplicate files in a selected directory. The program computes file hashes (MD5) to detect identical files and allows users to delete unwanted duplicates.

## Features

- **Find Duplicate Files**: Quickly identifies duplicate files in a given directory based on their content (using MD5 hash).
- **Graphical Interface**: Uses Tkinter for a user-friendly interface with no command-line input required.
- **Preview Before Deletion**: Displays duplicate files along with their originals, allowing you to select which duplicates to remove.
- **Safe Deletion**: Lets you confirm before any files are deleted.

## Requirements

- Python 3.x
- Tkinter (comes pre-installed with Python)
- hashlib (part of the Python standard library)

## Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/yourusername/duplicate-file-finder.git
   cd duplicate-file-finder
   ```

2. Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).

## Usage

1. Run the program by executing the Python script:
   ```bash
   python duplicate_finder.py
   ```

2. A window will appear where you can:
   - Select a directory to search for duplicate files.
   - View a list of duplicate files along with their original counterparts.
   - Choose duplicates to delete with a simple interface.

## How It Works

1. **Directory Selection**: Click the "Select" button to choose the directory you want to scan for duplicates.
2. **Duplicate Detection**: The program scans all files in the directory and subdirectories, computes the MD5 hash of each file, and identifies duplicates.
3. **Displaying Results**: Duplicates are displayed in a table, showing both the duplicate and the original file.
4. **Deleting Duplicates**: Select duplicates from the list and click "Delete Selected Duplicates" to remove them. Only the selected duplicates will be deleted, leaving the original file intact.

## Future Improvements

- Add support for filtering by file types or file sizes.
- Optimize performance for very large directories.
- Provide more options for hash algorithms.

## Authors

This project is developed by Alexandr Kulakov
