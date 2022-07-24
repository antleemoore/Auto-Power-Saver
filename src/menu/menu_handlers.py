import re
import subprocess
import tkinter
from system.config import Config
from system.notification import handle_notification_settings, send_notification
from system.power_plan import delete_power_plan, install_power_plan
from system.system import get_sys_folder, is_admin
from update.update_handlers import handle_auto_updates, handle_update_frequency

print("Initializing menu handlers...")
control = "%SystemRoot%\system32\control.exe"
config = Config(f'{get_sys_folder("HOME")}\Documents\\auto_power_saver_config.ini')
quit = False
print()


def check_quit_status():
    return quit


def on_delete(icon, item):
    global config
    print(f"Deleting power plan {str(item)}...")
    delete_power_plan(str(item), config)
    icon.update_menu()


def on_install(icon, item):
    global config
    print(f"Installing power plan {str(item)}...")
    install_power_plan(str(item), config)
    icon.update_menu()


def on_exit(icon, item):
    global quit
    print("Exit option selected")
    icon.stop()
    quit = True


def on_win_power_settings(icon, item):
    print("Opening Windows Power Settings...")
    subprocess.call(f"{control} /name Microsoft.PowerOptions", shell=True)


def on_notifications(icon, item):
    global config
    print("Notifications option selected")
    handle_notification_settings(config)
    icon.update_menu()


def on_auto_updates(icon, item):
    global config
    print("Automatic updates option selected")
    handle_auto_updates(config)
    if config.automatic_updates == True and not is_admin():
        # tkinter message to show that the automatic updates are enabled
        tkinter.messagebox.showinfo(
            "Auto Power Saver",
            "In order for automatic updates to work properly, you need to restart the application as an administrator.",
        )
    icon.update_menu()


def on_release_frequency(icon, item):
    global config
    print("Update frequency option selected")
    handle_update_frequency(str(item), config)
    icon.update_menu()


def on_change_timer(icon, item):
    global config
    choice = int(re.search(r"\d+", str(item)).group())
    config.timeout = choice
    print("Changing timeout to " + str(choice))
    config.write_to_config()
    send_notification(
        f"The timeout length was changed to {int(config.timeout)} minutes.",
        config=config,
    )
    icon.update_menu()
