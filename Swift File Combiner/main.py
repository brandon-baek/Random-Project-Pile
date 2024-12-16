import tkinter as tk
from tkinter import filedialog
import os


def merge_swift_files(file_paths):
    merged_content = ""

    for file_path in file_paths:
        if os.path.isfile(file_path) and file_path.endswith(".swift"):
            # Extract the file name
            file_name = os.path.basename(file_path)

            # Read the file content
            with open(file_path, 'r') as file:
                file_content = file.read()

            # Append the file name and content to the merged content
            merged_content += f"{file_name}:\n\n\n{file_content}\n\n\n\n\n\n"
        else:
            print(f"Skipped non-Swift file: {file_path}")

    return merged_content


def get_all_swift_files_in_directory(directory):
    swift_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".swift"):
                swift_files.append(os.path.join(root, file))
    return swift_files


def select_files():
    # Allow the user to select multiple Swift files
    file_paths = filedialog.askopenfilenames(title="Select Swift Files", filetypes=[("Swift files", "*.swift")])

    if file_paths:
        process_files(list(file_paths))  # Convert to list in case it's not a list already
    else:
        print("No files selected.")


def select_folder():
    # Allow the user to select a folder
    folder_path = filedialog.askdirectory(title="Select a Folder Containing Swift Files")

    if folder_path:
        swift_files = get_all_swift_files_in_directory(folder_path)
        process_files(swift_files)
    else:
        print("No folder selected.")


def process_files(file_paths):
    if file_paths:
        merged_content = merge_swift_files(file_paths)
        text_area.delete(1.0, tk.END)  # Clear the text area
        text_area.insert(tk.END, merged_content)  # Insert the merged content
    else:
        print("No Swift files to process.")


# Initialize the tkinter window
root = tk.Tk()
root.title("Swift File Merger")

# Create a button to select individual Swift files
file_button = tk.Button(root, text="Select Swift Files", command=select_files)
file_button.pack(pady=10)

# Create a button to select a folder containing Swift files
folder_button = tk.Button(root, text="Select Folder Containing Swift Files", command=select_folder)
folder_button.pack(pady=10)

# Create a text area to display the merged content
text_area = tk.Text(root, height=20, width=80)
text_area.pack(padx=20, pady=20)

# Start the tkinter main loop
root.mainloop()
