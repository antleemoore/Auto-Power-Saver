from os import walk, path, startfile
from sys import exit
from timeit import default_timer as timer
from tkinter import messagebox, simpledialog
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk

from system.system import get_sys_folder, resource_path

executors_list = []

search_results = ""


def find_file(r, f, inp):
    global search_results
    for file in f:
        fp = ""
        if inp in file:
            fp = path.join(r, file)
            search_results += fp + "\n"


def menu_item_run_search():
    global search_results
    search_results = ""
    drive = simpledialog.askstring("File Search", "Which drive do you want to search?\n\n Example: C")
    if not drive:
        return
    inp = simpledialog.askstring("File Search", "Enter the file name you want to search for:\n\n Example: example.txt")
    if not inp:
        return

    root = tk.Tk()
    root.title("Auto Power Saver - Deep File Search")
    root.geometry("400x100")
    label = tk.Label(root, text="Waiting for the deep search to finish...")
    label.pack()
    root.after(200, run_search, root, inp, drive)
    root.mainloop()

    with open(f'{get_sys_folder("TEMP")}\\auto_power_saver_search_results.txt', "w") as f:
        f.write(search_results)
    startfile(f'{get_sys_folder("TEMP")}\\auto_power_saver_search_results.txt')


def run_search(root, inp, drive):
    print("Search is starting...")
    start = timer()
    with ThreadPoolExecutor() as executor:
        for r, d, f in walk(f"{drive}:\\"):
            executors_list.append(executor.submit(find_file, r, f, inp))
    print(f"Search took {timer() - start} seconds.")
    root.destroy()
