import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, MULTIPLE, END
import zipfile
import rarfile
from datetime import datetime

def get_file_checksum(file_path, algorithm='md5'):
    """Вычислить хэш-сумму файла"""
    hash_algo = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def scan_directory_for_files(directory):
    """Сканировать директорию и извлечь все файлы"""
    file_info = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_stat = os.stat(file_path)
                checksum = get_file_checksum(file_path)
                file_info[file_path] = {
                    'name': file,
                    'size': file_stat.st_size,
                    'checksum': checksum,
                    'created': file_stat.st_ctime,
                    'modified': file_stat.st_mtime
                }
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    return file_info

def scan_archives(directory):
    """Сканировать .zip и .rar архивы"""
    archive_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as zipf:
                    for info in zipf.infolist():
                        extracted_file = zipf.open(info)
                        file_data = extracted_file.read()
                        checksum = hashlib.md5(file_data).hexdigest()
                        archive_files.append((file_path, info.filename, info.file_size, 'zip', checksum))
            elif rarfile.is_rarfile(file_path):
                with rarfile.RarFile(file_path, 'r') as rarf:
                    for info in rarf.infolist():
                        extracted_file = rarf.open(info)
                        file_data = extracted_file.read()
                        checksum = hashlib.md5(file_data).hexdigest()
                        archive_files.append((file_path, info.filename, info.file_size, 'rar', checksum))
    return archive_files

def find_duplicates(files):
    """Найти дублирующие файлы"""
    duplicates = {}
    seen = {}
    for path, info in files.items():
        key = (info['size'], info['checksum'])
        if key in seen:
            if key not in duplicates:
                duplicates[key] = [seen[key]]
            duplicates[key].append(path)
        else:
            seen[key] = path
    return duplicates

def delete_files(file_list):
    """Удалить выбранные файлы"""
    for file in file_list:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Error deleting {file}: {e}")

# GUI
class DuplicateFileCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate Files Checker")
        self.root.geometry("600x455")
        
        self.directory_label = tk.Label(root, text="Directory:")
        self.directory_label.pack(pady=5)
        
        self.directory_entry = tk.Entry(root, width=50)
        self.directory_entry.pack(pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(pady=5)
        
        self.scan_button = tk.Button(root, text="Scan for Duplicates", command=self.scan_for_duplicates)
        self.scan_button.pack(pady=10)
        
        self.file_listbox = Listbox(root, selectmode=MULTIPLE, width=80, height=15)
        self.file_listbox.pack(pady=10)
        
        self.delete_button = tk.Button(root, text="Delete Selected Files", command=self.delete_selected_files)
        self.delete_button.pack(pady=5)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, END)
            self.directory_entry.insert(0, directory)

    def scan_for_duplicates(self):
        directory = self.directory_entry.get()
        if not directory or not os.path.exists(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return
        
        files = scan_directory_for_files(directory)
        archives = scan_archives(directory)
        
        for archive_file in archives:
            files[archive_file[0] + ":" + archive_file[1]] = {
                'name': archive_file[1],
                'size': archive_file[2],
                'checksum': archive_file[4],
                'created': datetime.now().timestamp(),
                'modified': datetime.now().timestamp()
            }
        
        duplicates = find_duplicates(files)
        
        self.file_listbox.delete(0, END)
        
        if duplicates:
            for key, file_list in duplicates.items():
                self.file_listbox.insert(END, f"Duplicate group: {key}")
                for file in file_list:
                    self.file_listbox.insert(END, f"  {file}")
        else:
            self.file_listbox.insert(END, "No duplicates found.")

    def delete_selected_files(self):
        selected = self.file_listbox.curselection()
        files_to_delete = [self.file_listbox.get(i).strip() for i in selected if not self.file_listbox.get(i).startswith("Duplicate group:")]
        
        if files_to_delete:
            confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected files?")
            if confirm:
                delete_files(files_to_delete)
                messagebox.showinfo("Success", "Selected files deleted.")
                self.scan_for_duplicates()  # Refresh the list after deletion

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFileCheckerApp(root)
    root.mainloop()


