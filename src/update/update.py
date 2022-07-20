import re
import os
import subprocess
import urllib.request
import requests
import semver
from tkinter import *
import tkinter.messagebox
from system.notification import send_notification
from system.system import get_powershell_path, get_sys_folder, resource_path


def download(url: str, dest_folder: str):
    print("Starting download...")
    if not os.path.exists(dest_folder):
        print("Creating destination folder...")
        os.makedirs(dest_folder)  # create folder if it does not exist

    # be careful with file names
    print("Setting file name...")
    filename = url.split("/")[-1].replace(" ", "_")
    print("Setting file path...")
    file_path = os.path.join(dest_folder, filename)
    print(f"Requesting file from {url}...")
    r = requests.get(url, stream=True)
    if r.ok:
        print("Saving to", os.path.abspath(file_path))
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def get_app_update_versions():
    try:
        webUrl = urllib.request.urlopen("https://raw.githubusercontent.com/antleemoore/Auto-Power-Saver/main/version")
        data = webUrl.read()
        version_file = open(f"{resource_path('version')}", "r")
        version = version_file.read()
        app_version = re.search(r"([\d.]+)", str(version)).group(1)
        update_version = re.search(r"\s*([\d.]+)", str(data)).group(1)
        return app_version, update_version
    except:
        print(f"Error getting update versions.")
        return "0.0.0", "0.0.0"


def check_for_updates(config):
    app_version, update_version = get_app_update_versions()
    current_major, current_minor, current_bug = map(int, app_version.split("."))
    new_major, new_minor, new_bug = map(int, update_version.split("."))
    print(f"Comparing versions: {current_major}.{current_minor}.{current_bug} to {new_major}.{new_minor}.{new_bug}")
    if semver.compare(update_version, app_version) == 1:
        if config.update_frequency == 1 and new_major <= current_major:
            return
        elif config.update_frequency == 2 and new_major >= current_major and new_minor <= current_minor:
            return
        else:
            pass
        if config.automatic_updates == True:
            print("Starting automatic update...")
            send_notification(
                f"Auto Power Saver is now updating to version {update_version}.",
                config=config,
            )
            on_check_updates(None, None)
        else:
            result = tkinter.messagebox.askquestion(
                "Auto Power Saver Update",
                f"Version {update_version} is available.  Do you want to update now?\nThe update will be handled in the background.",
            )
            if result == "yes":
                print("Starting manual update...")
                on_check_updates(None, None)
        return True
    else:
        print("Software is currently up to date.")
        return False


def on_check_updates(icon, item):
    app_version, update_version = get_app_update_versions()
    print("Getting update download url...")
    url = "https://raw.githubusercontent.com/antleemoore/Auto-Power-Saver/main/update"
    webUrl = urllib.request.urlopen(url)
    update_data = webUrl.read()
    update_exe = re.findall("http.*exe", str(update_data))
    download(str(update_exe[0]), f'{get_sys_folder("TEMP")}')
    print("Calling download PS command...")
    subprocess.call(
        f"{get_powershell_path()} Stop-Process -name 'Auto Power Saver' && {get_powershell_path()} {get_sys_folder('TEMP')}\\autopowersaver_setup__v{update_version}.exe /VERYSILENT",
        shell=True,
    )
    return True
