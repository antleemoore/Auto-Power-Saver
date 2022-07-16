import sys
from time import sleep
from datetime import datetime as dt
from tkinter import *
from system.power_plan import set_plan
from system.system import get_ac_status, get_idle_duration, is_admin
from update.update import check_for_updates
from menu.menu_icon import icon, activeplan, config, update
from menu.menu_handlers import config, check_quit_status


def init():
    set_plan(activeplan, config)
    icon.run_detached()


def run():
    global activeplan, update
    sleep(0.5)
    if check_quit_status():
        sys.exit()
    else:
        new_plan = activeplan

        if dt.now().minute % 15 == 0 and dt.now().second == 0:
            update = check_for_updates(config)

        if get_idle_duration() <= (config.timeout * 60) and get_ac_status().ACLineStatus == 1:
            new_plan = "High performance"
        else:
            new_plan = "Power saver"

        if activeplan == new_plan:
            pass
        else:
            activeplan = new_plan
            set_plan(activeplan, config)
    sleep(0.5)


init()
while True:
    run()
    sleep(0.5)
