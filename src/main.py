import sys
from time import sleep
from datetime import datetime as dt
from tkinter import *
import tkinter
from system.power_plan import set_plan
from system.system import get_ac_status, get_idle_duration, is_admin
from ui.index import open_window
from update.update import check_for_updates
from menu.menu_icon import icon, activeplan, update
from menu.menu_handlers import config, check_quit_status


def init():
    set_plan(activeplan, config)
    if not is_admin() and config.automatic_updates == True:
        tkinter.messagebox.showinfo(
            "Auto Power Saver",
            "In order for automatic updates to work properly, you need to restart the application as an administrator.",
        )
    print("Starting menu icon detached...")
    icon.run_detached()


def run():
    global activeplan, update
    sleep(0.5)
    if check_quit_status():
        print("Quitting Auto Power Saver...")
        sys.exit()
    else:
        new_plan = activeplan

        if dt.now().minute % 15 == 0 and dt.now().second == 0:
            print("Checking for updates...")
            update = check_for_updates(config)

        if get_idle_duration() <= (config.timeout * 60) and get_ac_status().ACLineStatus == 1:
            new_plan = "High performance"
        else:
            new_plan = "Power saver"

        if activeplan == new_plan:
            pass
        else:
            activeplan = new_plan
            print("Plan changed to " + activeplan)
            set_plan(activeplan, config)
    sleep(0.5)


init()
print("Running main application loop...")
while True:
    run()
    sleep(0.5)
