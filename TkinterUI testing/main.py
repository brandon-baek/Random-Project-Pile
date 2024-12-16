import tkinter as tk
import ttkbootstrap as ttk

def convert():
    miles = entry_int.get()
    output_string.set(str(miles * 1.61))

window = ttk.Window(themename = 'darkly')
window.title("User interface")
window.geometry('400x200')

title = ttk.Label(master = window, text = 'Miles to Kilometers', font = 'Calibri 24 bold')
title.pack(pady=10)

input_frame = ttk.Frame(master = window)
entry_int = tk.IntVar()
entry = ttk.Entry(master = input_frame, textvariable = entry_int)
button = ttk.Button(master = input_frame, text = 'Convert', command = convert)
entry.pack(side='left')
button.pack(side='left')
input_frame.pack(pady=5)

output_string = tk.StringVar()
output = ttk.Label(master = window, text = 'output', font = 'Calibri 24', textvariable = output_string)
output.pack()

tk.mainloop()