from os import startfile
import subprocess
from timeit import default_timer as timer
from tkinter import simpledialog
import tkinter as tk
import tkinter

from system.system import get_sys_folder, resource_path
import string
from ctypes import windll


search_results = ""


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    print("Available drives: " + str(drives))
    return drives


def menu_item_run_search():
    global search_results
    search_results = ""
    # tkinter se
    print("Getting drive data from user...")
    drive = simpledialog.askstring("File Search", "Which drive do you want to search?\n\n Example: C")
    if not drive:
        return
    if drive not in get_drives():
        tkinter.messagebox.showinfo("File Search", "You need to enter a valid drive letter.")
        return
    print(f"Selected drive: {drive}")
    print("Getting file name from user...")
    inp = simpledialog.askstring("File Search", "Enter the file name you want to search for:\n\n Example: example.txt")
    if not inp:
        tkinter.messagebox.showinfo("File Search", "You didn't enter a file name.")
        return
    print("File to search for: " + inp)
    root = tk.Tk()
    root.title("Auto Power Saver - Deep File Search")
    root.geometry("300x100")
    label = tk.Label(root, text="Waiting for the deep search to finish...")
    label.pack()
    root.after(200, run_search, root, inp, drive + ":\\")
    root.mainloop()
    print(f"Writing search results to {get_sys_folder('TEMP')}\\auto_power_saver_search_results.txt...")
    with open(f'{get_sys_folder("TEMP")}\\auto_power_saver_search_results.txt', "w") as f:
        f.write(search_results)
    startfile(f'{get_sys_folder("TEMP")}\\auto_power_saver_search_results.txt')


def run_search(root, inp, drive):
    global search_results
    start = timer()
    # run resources/additional features/file_search.exe using subprocess and store the printed output in search_results
    print("Running deep file search...")
    search_results = subprocess.check_output(
        [resource_path("resources/additional_features/file_search.exe"), inp, drive],
        shell=True,
        universal_newlines=True,
    )
    print(f"Search finished in {timer() - start} seconds.")
    print(f"\nSearch results:\n{search_results}")
    root.destroy()
