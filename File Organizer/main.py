import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import ttkbootstrap as ttk
import json


class FileOrganizerApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("File Organizer")
        self.geometry("800x600")

        self.source_dirs = []
        self.organized_dirs = set()
        self.moved_files_history = []
        self.undo_history = []

        self.load_settings()
        self.create_widgets()

    def load_settings(self):
        default_settings = {
            "file_types": {
                "Images": {
                    "extensions": [".jpg", ".jpeg", ".png", ".gif"],
                    "destination": os.path.expanduser("~/Pictures")
                },
                "Documents": {
                    "extensions": [".pdf", ".doc", ".docx", ".txt"],
                    "destination": os.path.expanduser("~/Documents")
                },
                "Videos": {
                    "extensions": [".mp4", ".mov", ".avi"],
                    "destination": os.path.expanduser("~/Videos")
                }
            }
        }
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
            if 'file_types' not in self.settings:
                self.settings['file_types'] = default_settings['file_types']
        except FileNotFoundError:
            self.settings = default_settings

        self.save_settings()

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4)

    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.tab_buttons_frame = ttk.Frame(self.main_frame)
        self.tab_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.organizer_frame = ttk.Frame(self.content_frame)
        self.settings_frame = ttk.Frame(self.content_frame)

        self.organizer_button = ttk.Button(self.tab_buttons_frame, text="Organizer",
                                           command=lambda: self.show_frame("organizer"), style="TButton")
        self.organizer_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.settings_button = ttk.Button(self.tab_buttons_frame, text="Settings",
                                          command=lambda: self.show_frame("settings"), style="TButton")
        self.settings_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.create_organizer_widgets()
        self.create_settings_widgets()

        self.show_frame("organizer")

    def show_frame(self, frame_name):
        if frame_name == "organizer":
            self.settings_frame.pack_forget()
            self.organizer_frame.pack(fill=tk.BOTH, expand=True)
            self.organizer_button.state(["pressed"])
            self.settings_button.state(["!pressed"])
        elif frame_name == "settings":
            self.organizer_frame.pack_forget()
            self.settings_frame.pack(fill=tk.BOTH, expand=True)
            self.settings_button.state(["pressed"])
            self.organizer_button.state(["!pressed"])

    def create_organizer_widgets(self):
        title_label = ttk.Label(self.organizer_frame, text="File Organizer", font=("TkDefaultFont", 24, "bold"))
        title_label.pack(pady=(20, 20))

        select_button = ttk.Button(self.organizer_frame, text="Select Source Folder", command=self.select_folder)
        select_button.pack(fill=tk.X, padx=20, pady=5)

        self.folders_frame = ttk.Frame(self.organizer_frame)
        self.folders_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        button_frame = ttk.Frame(self.organizer_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=5)

        organize_button = ttk.Button(button_frame, text="Organize Files", command=self.run_organizer)
        organize_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        undo_button = ttk.Button(button_frame, text="Undo", command=self.undo_organization)
        undo_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        redo_button = ttk.Button(button_frame, text="Redo", command=self.redo_organization)
        redo_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

    def create_settings_widgets(self):
        self.settings_canvas = ttk.Canvas(self.settings_frame)
        self.settings_scrollbar = ttk.Scrollbar(self.settings_frame, orient="vertical",
                                                command=self.settings_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.settings_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.settings_canvas.configure(
                scrollregion=self.settings_canvas.bbox("all")
            )
        )

        self.settings_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.settings_canvas.configure(yscrollcommand=self.settings_scrollbar.set)

        self.settings_canvas.pack(side="left", fill="both", expand=True)
        self.settings_scrollbar.pack(side="right", fill="y")

        title_label = ttk.Label(self.scrollable_frame, text="File Type Settings", font=("TkDefaultFont", 24, "bold"))
        title_label.pack(pady=(20, 20))

        self.file_type_frames = {}

        for file_type, data in self.settings["file_types"].items():
            self.create_file_type_frame(file_type, data)

        add_type_button = ttk.Button(self.scrollable_frame, text="Add New File Type", command=self.add_new_file_type)
        add_type_button.pack(pady=10)

        save_button = ttk.Button(self.scrollable_frame, text="Save Settings", command=self.save_settings_from_ui)
        save_button.pack(pady=20)

    def create_file_type_frame(self, file_type, data):
        frame = ttk.LabelFrame(self.scrollable_frame, text=file_type)
        frame.pack(fill=tk.X, padx=20, pady=5)

        extensions_label = ttk.Label(frame, text="Extensions:")
        extensions_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        extensions_entry = ttk.Entry(frame, width=30)
        extensions_entry.insert(0, ", ".join(data["extensions"]))
        extensions_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        destination_label = ttk.Label(frame, text="Destination:")
        destination_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        destination_entry = ttk.Entry(frame, width=30)
        destination_entry.insert(0, data["destination"])
        destination_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        browse_button = ttk.Button(frame, text="Browse", command=lambda e=destination_entry: self.browse_folder(e))
        browse_button.grid(row=1, column=2, padx=5, pady=5)

        remove_button = ttk.Button(frame, text="Remove", command=lambda: self.remove_file_type(file_type))
        remove_button.grid(row=2, column=1, pady=5)

        frame.grid_columnconfigure(1, weight=1)

        self.file_type_frames[file_type] = {
            "frame": frame,
            "extensions": extensions_entry,
            "destination": destination_entry
        }

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder and folder not in self.source_dirs:
            self.source_dirs.append(folder)
            self.update_folder_list()

    def update_folder_list(self):
        for widget in self.folders_frame.winfo_children():
            widget.destroy()

        for i, folder in enumerate(self.source_dirs):
            frame = ttk.Frame(self.folders_frame)
            frame.pack(fill=tk.X, pady=2)

            status = "✓ Organized" if folder in self.organized_dirs else ""
            label = ttk.Label(frame, text=f"{folder} {status}", anchor="w")
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            remove_button = ttk.Button(frame, text="X", width=3,
                                       command=lambda idx=i: self.remove_folder(idx))
            remove_button.pack(side=tk.RIGHT)

    def remove_folder(self, index):
        folder = self.source_dirs[index]
        del self.source_dirs[index]
        self.organized_dirs.discard(folder)
        self.update_folder_list()

    def add_new_file_type(self):
        new_type = simpledialog.askstring("New File Type", "Enter name for new file type:")
        if new_type:
            self.settings["file_types"][new_type] = {
                "extensions": [],
                "destination": os.path.expanduser("~")
            }
            self.create_file_type_frame(new_type, self.settings["file_types"][new_type])
            self.settings_canvas.update_idletasks()
            self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all"))

    def remove_file_type(self, file_type):
        if file_type in self.file_type_frames:
            self.file_type_frames[file_type]["frame"].destroy()
            del self.file_type_frames[file_type]
            del self.settings["file_types"][file_type]
            self.settings_canvas.update_idletasks()
            self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox("all"))

    def browse_folder(self, entry):
        folder = filedialog.askdirectory()
        if folder:
            entry.delete(0, tk.END)
            entry.insert(0, folder)

    def save_settings_from_ui(self):
        for file_type, entries in self.file_type_frames.items():
            extensions = [ext.strip() for ext in entries["extensions"].get().split(",")]
            destination = entries["destination"].get()
            self.settings["file_types"][file_type] = {
                "extensions": extensions,
                "destination": destination
            }
        self.save_settings()
        messagebox.showinfo("Settings Saved", "Your settings have been saved successfully!")

    def run_organizer(self):
        if not self.source_dirs:
            messagebox.showwarning("No folders selected", "Please select at least one source folder.")
            return

        new_moved_files = self.organize_files(self.source_dirs)
        self.moved_files_history.append(new_moved_files)
        self.undo_history.clear()
        self.organized_dirs.update(self.source_dirs)
        self.update_folder_list()
        messagebox.showinfo("Success", "Files have been organized successfully!")

    def organize_files(self, source_dirs):
        moved_files = {}

        for source_dir in source_dirs:
            moved_files[source_dir] = []
            for filename in os.listdir(source_dir):
                file_path = os.path.join(source_dir, filename)

                if not os.path.isfile(file_path):
                    continue

                _, extension = os.path.splitext(filename)
                extension = extension.lower()

                dest_path = self.get_destination_path(extension, filename)

                if dest_path:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(file_path, dest_path)
                    moved_files[source_dir].append((file_path, dest_path))

        return moved_files

    def get_destination_path(self, extension, filename):
        for file_type, data in self.settings["file_types"].items():
            if extension in data["extensions"]:
                return os.path.join(data["destination"], filename)
        return None

    def undo_organization(self):
        if not self.moved_files_history:
            messagebox.showwarning("Nothing to undo", "No organization has been performed yet.")
            return

        moved_files = self.moved_files_history.pop()
        self.undo_files(moved_files)
        self.undo_history.append(moved_files)
        self.organized_dirs = set(self.moved_files_history[-1].keys()) if self.moved_files_history else set()
        self.update_folder_list()
        messagebox.showinfo("Success", "Last organization has been undone successfully!")

    def undo_files(self, moved_files):
        for source_dir, files in moved_files.items():
            for original_path, current_path in files:
                if os.path.exists(current_path):
                    shutil.move(current_path, original_path)

    def redo_organization(self):
        if not self.undo_history:
            messagebox.showwarning("Nothing to redo", "No undo action to redo.")
            return

        moved_files = self.undo_history.pop()
        new_moved_files = self.organize_files(moved_files.keys())
        self.moved_files_history.append(new_moved_files)
        self.organized_dirs.update(new_moved_files.keys())
        self.update_folder_list()
        messagebox.showinfo("Success", "Organization has been redone successfully!")


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
