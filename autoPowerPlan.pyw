from ctypes import Structure, windll, c_uint, sizeof, byref
import subprocess
import re
import sys
import os
from time import sleep
import pystray
import PIL.Image
from notifypy import Notify
from configparser import ConfigParser
from os.path import expanduser
home = expanduser("~")
running = True
quit = False

config = ConfigParser()
config.read(f'{home}\Documents\\auto_power_saver_config.ini')
try:
    config.get('main', 'timeout')
    config.get('main', 'disable_notifications')
except:
    if not config.has_section('main'):
        config.add_section('main')
    config.set('main', 'timeout', '3') 
    config.set('main', 'disable_notifications', 'False')
timer = 60 * int(config.get('main', 'timeout'))
enabled = timer / 60
with open(f'{home}\Documents\\auto_power_saver_config.ini', 'w') as f:
    config.write(f)

disable_notifications = True if config.get('main', 'disable_notifications') == "True" else False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

image = PIL.Image.open(resource_path("green_power.jpeg"))

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]
def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0
def get_plans():
    cmd_output = str(subprocess.check_output("%SystemRoot%\system32\WindowsPowerShell\\v1.0\powershell.exe powercfg /list",shell=True))
    powerplans = re.findall(r'\((.*?) *\)', cmd_output)
    powerplans.pop(0)
    guid = re.findall(r'(?<=GUID: ).*?(?=\s)', cmd_output)
    guid = [x for x in guid if x != '']
    options = {}
    for i in range(powerplans.__len__()):
        options[powerplans[i]] = guid[i]
    return options
plans = get_plans()
def set_plan(name):
    try:
        str(subprocess.call(f"%SystemRoot%\system32\WindowsPowerShell\\v1.0\powershell.exe powercfg /setactive {plans[name]}",shell=True))
        send_notification(f"The power plan was switched to {name}")
    except:
        send_notification(f"You are missing the {name} power plan.  Create it in settings.")
        return False
    return True
def send_notification(msg):
    if disable_notifications == True:
        return
    notification = Notify()
    notification.title = f"Auto Power Saver"
    notification.message = msg
    notification.icon = resource_path("green_power.jpeg")
    notification.send()   
def on_clicked(icon, item):
    global running, activeplan, quit, disable_notifications
    if str(item) == "Exit":
        running = False
        icon.stop()
        quit = True
    elif str(item) == "Edit power plan settings":
        subprocess.call("%SystemRoot%\system32\control.exe /name Microsoft.PowerOptions",shell=True)
    elif str(item) == "High performance":
        subprocess.call(f'{resource_path("get_high_performance_power_plan.bat")}', shell=True)
        send_notification("High performance power plan has been downloaded.")
    elif str(item) == "Power saver":
        subprocess.call(f'{resource_path("get_power_saver_power_plan.bat")}', shell=True)   
        send_notification("Power saver power plan has been downloaded.")
    elif str(item) == "Disable notifications":
        disable_notifications = True if disable_notifications == False else False
        config.set('main', 'disable_notifications', f'{"True" if disable_notifications == True else "False"}')
        if disable_notifications == False:
            send_notification("Notifications have been enabled.")
    with open(f'{home}\Documents\\auto_power_saver_config.ini', 'w') as f:
        config.write(f)
    icon.update_menu()  
def on_change_timer(icon, item):
    global enabled, timer, config
    if str(item) == "1 minute":
        enabled = 1
        timer = 60
    elif str(item) == "2 minutes":
        enabled = 2
        timer = 60 * 2
    elif str(item) == "3 minutes":
        enabled = 3
        timer = 60 * 3
    elif str(item) == "5 minutes":
        enabled = 5
        timer = 60 * 5
    elif str(item) == "10 minutes":
        enabled = 10
        timer = 60 * 10
    elif str(item) == "15 minutes":
        enabled = 15
        timer = 60 * 15
    elif str(item) == "30 minutes":
        enabled = 30
        timer = 60 * 30
    elif str(item) == "60 minutes":
        enabled = 60
        timer = 60 * 60
    elif str(item) == "120 minutes":
        enabled = 120
        timer = 60 * 120
    config.set('main', 'timeout', str(int(timer/60)))
    with open(f'{home}\Documents\\auto_power_saver_config.ini', 'w') as f:
        config.write(f)
    send_notification(f"The timeout length was changed to {int(timer / 60)} minutes.")

activeplan = "High performance"
set_plan(activeplan)

icon = pystray.Icon("Auto Power Saver", image, menu=pystray.Menu(
    pystray.MenuItem("Settings", pystray.Menu(
        pystray.MenuItem("Edit power plan settings", on_clicked),
        pystray.MenuItem("Disable notifications", on_clicked, checked=lambda item: disable_notifications == True),
        pystray.MenuItem("Create power plan", pystray.Menu(
            pystray.MenuItem("High performance", on_clicked, checked=lambda item: plans.get("High performance") != None),
            pystray.MenuItem("Power saver", on_clicked, checked=lambda item: plans.get("Power saver") != None),
            )),
        pystray.MenuItem("Change timeout", pystray.Menu(
            pystray.MenuItem("1 minute", on_change_timer, radio=True, checked=lambda item: enabled == 1),
            pystray.MenuItem("2 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 2),
            pystray.MenuItem("3 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 3),
            pystray.MenuItem("5 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 5),
            pystray.MenuItem("10 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 10),
            pystray.MenuItem("15 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 15),
            pystray.MenuItem("30 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 30),
            pystray.MenuItem("60 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 60),
            pystray.MenuItem("120 minutes", on_change_timer, radio=True, checked=lambda item: enabled == 120)
        )) 
    )),
    pystray.MenuItem("Exit", on_clicked)  
))
icon.run_detached()
while True:
    sleep(0.5)
    if quit:
        sys.exit()
    if running:
        new_plan = activeplan
        if get_idle_duration() <= timer: 
            new_plan = "High performance"
        else:
            new_plan = "Power saver"
        
        if activeplan == new_plan:
            continue
        else:
            activeplan = new_plan
            set_plan(activeplan)
    sleep(0.5)

