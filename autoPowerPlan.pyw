import ctypes
from ctypes import Structure, windll, c_uint, sizeof, byref, wintypes
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
import urllib.request
import requests
from datetime import datetime as dt
import semver
import tempfile
from tkinter import * 
import tkinter.messagebox 

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', wintypes.BYTE),
        ('BatteryFlag', wintypes.BYTE),
        ('BatteryLifePercent', wintypes.BYTE),
        ('Reserved1', wintypes.BYTE),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
    ]

SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
TEMP_FOLDER = tempfile.gettempdir()  
GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
GetSystemPowerStatus.restype = wintypes.BOOL

status = SYSTEM_POWER_STATUS()
if not GetSystemPowerStatus(ctypes.pointer(status)):
    raise ctypes.WinError()

running = True
quit = False
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def send_notification(msg):
    if disable_notifications == True:
        return
    notification = Notify()
    notification.title = f"Auto Power Saver"
    notification.message = msg
    notification.icon = resource_path("green_power.jpeg")
    notification.send()   
update = False
app_version = 0
update_version = 0
def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
def on_check_updates(icon, item):
    global quit, app_version
    url = 'https://raw.githubusercontent.com/antleemoore/Auto-Power-Saver/main/update'
    webUrl  = urllib.request.urlopen(url)
    update_data = webUrl.read()
    update_exe = re.findall('http.*exe', str(update_data))
    print(str(update_exe[0]))

    download(str(update_exe[0]), f'{TEMP_FOLDER}')
    subprocess.call(f"%SystemRoot%\system32\WindowsPowerShell\\v1.0\powershell.exe Stop-Process -name 'Auto Power Saver' && %SystemRoot%\system32\WindowsPowerShell\\v1.0\powershell.exe {TEMP_FOLDER}\\autopowersaver_setup__v{update_version}.exe /VERYSILENT",shell=True)
    quit = True
def on_reinstall(icon, item):
    global plans
    if str(item) == "High performance":
        subprocess.call(f'powercfg /delete {plans.get("High performance")}', shell=True)
        send_notification("High performance power plan has been deleted.")
    elif str(item) == "Power saver":
        subprocess.call(f'powercfg /delete {plans.get("Power saver")}', shell=True)   
        send_notification("Power saver power plan has been deleted.")
    plans = get_plans()
    icon.update_menu()
home = expanduser("~")
config = ConfigParser()
config.read(f'{home}\Documents\\auto_power_saver_config.ini')
try:
    config.get('main', 'timeout')
    config.get('main', 'disable_notifications')
    config.get('main', 'update_frequency')
except:
    if not config.has_section('main'):
        config.add_section('main')
    config.set('main', 'timeout', '3') 
    config.set('main', 'disable_notifications', 'False')
    config.set('main', 'update_frequency', '3')
timer = 60 * int(config.get('main', 'timeout'))
update_status = int(config.get('main', 'update_frequency'))
enabled = timer / 60
with open(f'{home}\Documents\\auto_power_saver_config.ini', 'w') as f:
    config.write(f)
def check_for_updates():
    global update, app_version, update_version
    webUrl  = urllib.request.urlopen('https://raw.githubusercontent.com/antleemoore/Auto-Power-Saver/main/version')
    data = webUrl.read()
    version_file = open(f"{resource_path('version')}", "r")
    version = version_file.read()
    app_version =  re.search(r'([\d.]+)', str(version)).group(1)
    update_version = re.search(r'\s*([\d.]+)', str(data)).group(1)
    current_major, current_minor, current_bug = map(int, app_version.split('.'))
    new_major, new_minor, new_bug = map(int, update_version.split('.'))
    if semver.compare(update_version, app_version) == 1:
        if update_status == 1 and new_major <= current_major:
            return
        elif update_status == 2 and new_major >= current_major and new_minor <= current_minor:
            return
        else:
            pass
        result=tkinter.messagebox.askquestion('Update',f'Version {update_version} is available.  Do you want to update now?\nThe update will be handled in the background.')
        if result=='yes':
            on_check_updates(None, None)
        else:
            pass
    else:
        print('Software is currently up to date.')
check_for_updates()   








disable_notifications = True if config.get('main', 'disable_notifications') == "True" else False

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
        subprocess.call(f"%SystemRoot%\system32\WindowsPowerShell\\v1.0\powershell.exe powercfg /setactive {plans[name]}",shell=True)
        send_notification(f"The power plan was switched to {name}")
    except:
        send_notification(f"You are missing the {name} power plan.  Create it in settings.")
        return False
    return True
     


def on_clicked(icon, item):
    global running, activeplan, quit, disable_notifications,update_status, plans
    if str(item) == "Exit":
        running = False
        icon.stop()
        quit = True
    elif str(item) == "Edit power plan settings":
        subprocess.call("%SystemRoot%\system32\control.exe /name Microsoft.PowerOptions",shell=True)
    elif str(item) == "High performance":
        subprocess.call(f'{resource_path("get_high_performance_power_plan.bat")}', shell=True)
        send_notification("High performance power plan has been downloaded.")
        plans = get_plans()
    elif str(item) == "Power saver":
        subprocess.call(f'{resource_path("get_power_saver_power_plan.bat")}', shell=True)   
        send_notification("Power saver power plan has been downloaded.")
        plans = get_plans()
    elif str(item) == "Disable notifications":
        disable_notifications = True if disable_notifications == False else False
        config.set('main', 'disable_notifications', f'{"True" if disable_notifications == True else "False"}')
        if disable_notifications == False:
            send_notification("Notifications have been enabled.")
    elif str(item) == "Major releases":
        update_status = 1
        config.set('main', 'update_frequency', str(update_status))
    elif str(item) == "Minor releases":
        update_status = 2
        config.set('main', 'update_frequency', str(update_status))
    elif str(item) == "Bug fixes":
        update_status = 3
        config.set('main', 'update_frequency', str(update_status))
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

activeplan = "High performance" if status.ACLineStatus == 1 else "Power saver"
set_plan(activeplan)

icon = pystray.Icon("Auto Power Saver", image, menu=pystray.Menu(
    pystray.MenuItem(f"Version: {app_version}", on_check_updates, enabled = False),
    pystray.MenuItem("Update now", on_check_updates, enabled = lambda item : update == True),
    pystray.MenuItem("Create power plan", pystray.Menu(
        pystray.MenuItem("High performance", on_clicked, checked=lambda item: plans.get("High performance") != None),
        pystray.MenuItem("Power saver", on_clicked, checked=lambda item: plans.get("Power saver") != None),
        )),
    pystray.MenuItem("Delete power plan", pystray.Menu(
        pystray.MenuItem("High performance", on_reinstall),
        pystray.MenuItem("Power saver", on_reinstall),
        )),
    pystray.MenuItem("Edit power plan settings", on_clicked),
    pystray.MenuItem("Disable notifications", on_clicked, checked=lambda item: disable_notifications == True),
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
    )), 
    pystray.MenuItem("Change update frequency", pystray.Menu(
        pystray.MenuItem("Major releases", on_clicked, radio=True, checked=lambda item: update_status == 1),
        pystray.MenuItem("Minor releases", on_clicked, radio=True, checked=lambda item: update_status == 2),
        pystray.MenuItem("Bug fixes", on_clicked, radio=True, checked=lambda item: update_status == 3),
    )), 
    pystray.MenuItem("Exit", on_clicked)  
))
icon.run_detached()
while True:
    sleep(0.5)
    if quit:
        sys.exit()
    if running:
        SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
        GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
        GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
        GetSystemPowerStatus.restype = wintypes.BOOL
        status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(ctypes.pointer(status)):
            raise ctypes.WinError()
        if dt.now().minute % 15 == 0 and dt.now().second == 0:
            check_for_updates()
            icon.update_menu()
        new_plan = activeplan
        if get_idle_duration() <= timer and status.ACLineStatus == 1: 
            new_plan = "High performance"
        else:
            new_plan = "Power saver"
        
        if activeplan == new_plan:
            continue
        else:
            activeplan = new_plan
            set_plan(activeplan)
    sleep(0.5)

