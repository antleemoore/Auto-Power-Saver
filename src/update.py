import subprocess
import re
import os
import urllib.request
import requests
import semver
from tkinter import *
import tkinter.messagebox
from notification import send_notification
from system import get_powershell_path, get_sys_folder, resource_path


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    # be careful with file names
    filename = url.split("/")[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


def get_app_update_versions():
    webUrl = urllib.request.urlopen(
        "https://raw.githubusercontent.com/antleemoore/Auto-Power-Saver/main/version"
    )
    data = webUrl.read()
    version_file = open(f"{resource_path('version')}", "r")
    version = version_file.read()
    app_version = re.search(r"([\d.]+)", str(version)).group(1)
    update_version = re.search(r"\s*([\d.]+)", str(data)).group(1)
    return app_version, update_version


def check_for_updates(config):
    app_version, update_version = get_app_update_versions()
    print(app_version, update_version)
    current_major, current_minor, current_bug = map(int, app_version.split("."))
    new_major, new_minor, new_bug = map(int, update_version.split("."))
    print(semver.compare(update_version, app_version))
    if semver.compare(update_version, app_version) == 1:
        if config.update_frequency == 1 and new_major <= current_major:
            return
        elif (
            config.update_frequency == 2
            and new_major >= current_major
            and new_minor <= current_minor
        ):
            return
        else:
            pass
        if config.automatic_updates == True:
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
                on_check_updates(None, None)
        return True
    else:
        print("Software is currently up to date.")
        return False


def on_check_updates(icon, item):
    app_version, update_version = get_app_update_versions()
    url = "https://raw.githubusercontent.com/antleemoore/Auto-Power-Saver/main/update"
    webUrl = urllib.request.urlopen(url)
    update_data = webUrl.read()
    update_exe = re.findall("http.*exe", str(update_data))
    print(str(update_exe[0]))

    download(str(update_exe[0]), f'{get_sys_folder("TEMP")}')
    subprocess.call(
        f"{get_powershell_path()} Stop-Process -name 'Auto Power Saver' && {get_powershell_path()} {get_sys_folder('TEMP')}\\autopowersaver_setup__v{update_version}.exe /VERYSILENT",
        shell=True,
    )
    return True


def handle_auto_updates(config):
    config.automatic_updates = True if config.automatic_updates == False else False
    config.config.set(
        "main",
        "automatic_updates",
        f'{"True" if config.automatic_updates == True else "False"}',
    )
    if config.automatic_updates == True:
        send_notification(
            "Auto Power Saver will now update automatically in the background.",
            config=config,
        )


def handle_update_frequency(name, config):
    if name == "Major releases":
        config.update_frequency = 1
        config.config.set("main", "update_frequency", str(config.update_frequency))
    elif name == "Minor releases":
        config.update_frequency = 2
        config.config.set("main", "update_frequency", str(config.update_frequency))
    elif name == "Bug fixes":
        config.update_frequency = 3
        config.config.set("main", "update_frequency", str(config.update_frequency))

    config.write_to_config()
