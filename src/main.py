import subprocess
import re
import sys
from time import sleep
import pystray
import PIL.Image
from datetime import datetime as dt
from tkinter import *
from config import Config
from notification import send_notification
from power_plan import get_plans, set_plan
from system import get_ac_status, get_idle_duration, resource_path
from update import check_for_updates, get_app_update_versions, on_check_updates

config = Config()
quit = False
enabled = config.timeout / 60
update = False
def on_reinstall(icon, item):
    if str(item) == "High performance":
        subprocess.call(
            f'powercfg /delete {get_plans().get("High performance")}', shell=True)
        send_notification("High performance power plan has been deleted.", config=config)
    elif str(item) == "Power saver":
        subprocess.call(
            f'powercfg /delete {get_plans().get("Power saver")}', shell=True)
        send_notification("Power saver power plan has been deleted.", config=config)
    icon.update_menu()

try:
    update = check_for_updates(config)
except:
    print("Unable to check for updates. Try reconnecting to the internet.")
image = PIL.Image.open(resource_path("green_power.jpeg"))

control = '%SystemRoot%\system32\control.exe'

def on_clicked(icon, item):
    global activeplan, quit, config
    if str(item) == "Exit":
        icon.stop()
        quit = True
    elif str(item) == "Edit Windows power plan settings":
        subprocess.call(f"{control} /name Microsoft.PowerOptions", shell=True)
    elif str(item) == "High performance":
        subprocess.call(
            f'{resource_path("get_high_performance_power_plan.bat")}', shell=True)
        send_notification("High performance power plan has been downloaded.", config=config)
    elif str(item) == "Power saver":
        subprocess.call(
            f'{resource_path("get_power_saver_power_plan.bat")}', shell=True)
        send_notification("Power saver power plan has been downloaded.", config=config)
    elif str(item) == "Disable notifications":
        config.disable_notifications = True if config.disable_notifications == False else False
        config.config.set('main', 'disable_notifications',
                   f'{"True" if config.disable_notifications == True else "False"}')
        if config.disable_notifications == False:
            send_notification("Notifications have been enabled.", config=config)
    elif str(item) == "Automatic updates":
        print(config.automatic_updates)
        config.automatic_updates = True if config.automatic_updates == False else False
        config.config.set('main', 'automatic_updates',
                   f'{"True" if config.automatic_updates == True else "False"}')
        if config.automatic_updates == True:
            send_notification(
                "Auto Power Saver will now update automatically in the background.", config=config)
    elif str(item) == "Major releases":
        config.update_frequency = 1
        config.config.set('main', 'update_frequency', str(config.update_frequency))
    elif str(item) == "Minor releases":
        config.update_frequency = 2
        config.config.set('main', 'update_frequency', str(config.update_frequency))
    elif str(item) == "Bug fixes":
        config.update_frequency = 3
        config.config.set('main', 'update_frequency', str(config.update_frequency))

    config.write_to_config()
    icon.update_menu()

def on_change_timer(icon, item):
    choice = int(re.search(r'\d+', str(item)).group())
    global enabled, config
    enabled = choice
    config.timeout = 60 * choice
    config.config.set('main', 'timeout', str(int(config.timeout/60)))
    config.write_to_config()
    send_notification(
        f"The timeout length was changed to {int(config.timeout / 60)} minutes.", config=config)

activeplan = "High performance" if get_ac_status(
).ACLineStatus == 1 else "Power saver"
set_plan(activeplan, config)
app_settings = pystray.Menu(
    pystray.MenuItem("Change timeout", pystray.Menu(
        pystray.MenuItem("1 minute", on_change_timer, radio=True,
                         checked=lambda item: enabled == 1),
        pystray.MenuItem("2 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 2),
        pystray.MenuItem("3 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 3),
        pystray.MenuItem("5 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 5),
        pystray.MenuItem("10 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 10),
        pystray.MenuItem("15 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 15),
        pystray.MenuItem("30 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 30),
        pystray.MenuItem("60 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 60),
        pystray.MenuItem("120 minutes", on_change_timer,
                         radio=True, checked=lambda item: enabled == 120)
    )),
    pystray.MenuItem("Change update frequency", pystray.Menu(
        pystray.MenuItem("Major releases", on_clicked, radio=True,
                         checked=lambda item: config.update_frequency == 1),
        pystray.MenuItem("Minor releases", on_clicked, radio=True,
                         checked=lambda item: config.update_frequency == 2),
        pystray.MenuItem("Bug fixes", on_clicked, radio=True,
                         checked=lambda item: config.update_frequency == 3),
    )),
)
power_settings = pystray.Menu(
    pystray.MenuItem("Create power plan", pystray.Menu(
        pystray.MenuItem("High performance", on_clicked, checked=lambda item: get_plans().get(
            "High performance") != None),
        pystray.MenuItem("Power saver", on_clicked,
                         checked=lambda item: get_plans().get("Power saver") != None),
    )),
    pystray.MenuItem("Delete power plan", pystray.Menu(
        pystray.MenuItem("High performance", on_reinstall),
        pystray.MenuItem("Power saver", on_reinstall),
    )),
    pystray.MenuItem("Edit Windows power plan settings", on_clicked),

)
app_version, update_version = get_app_update_versions()
icon = pystray.Icon("Auto Power Saver", image, title="Auto Power Saver", menu=pystray.Menu(
    pystray.MenuItem(f"Version: {app_version}",
                     on_check_updates, enabled=False),
    pystray.MenuItem(
        f"Current power plan: {activeplan}", on_check_updates, enabled=False),
    pystray.MenuItem("Update now", on_check_updates,
                     visible=lambda item: update == True),
    pystray.MenuItem("Disable notifications", on_clicked,
                     checked=lambda item: config.disable_notifications == True),
    pystray.MenuItem("Automatic updates", on_clicked,
                     checked=lambda item: config.automatic_updates == True),
    pystray.MenuItem("Power settings", power_settings),
    pystray.MenuItem("App settings", app_settings),
    pystray.MenuItem("Exit", on_clicked)
))

icon.run_detached()
while True:
    sleep(0.5)
    if quit:
        sys.exit()
    else:
        if dt.now().minute % 15 == 0 and dt.now().second == 0:
            update = check_for_updates(config)
            icon.update_menu()
        new_plan = activeplan
        if get_idle_duration() <= config.timeout and get_ac_status().ACLineStatus == 1:
            new_plan = "High performance"
        else:
            new_plan = "Power saver"

        if activeplan == new_plan:
            continue
        else:
            activeplan = new_plan
            set_plan(activeplan, config)
    sleep(0.5)
