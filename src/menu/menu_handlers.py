import re
import subprocess
from system.config import Config
from system.notification import handle_notification_settings, send_notification
from system.power_plan import delete_power_plan, install_power_plan
from system.system import get_sys_folder
from update.update_handlers import handle_auto_updates, handle_update_frequency

control = "%SystemRoot%\system32\control.exe"
config = Config(f'{get_sys_folder("HOME")}\Documents\\auto_power_saver_config.ini')
quit = False


def check_quit_status():
    return quit


def on_delete(icon, item):
    global config
    delete_power_plan(str(item), config)
    icon.update_menu()


def on_install(icon, item):
    global config
    install_power_plan(str(item), config)
    icon.update_menu()


def on_exit(icon, item):
    global quit
    icon.stop()
    quit = True


def on_win_power_settings(icon, item):
    subprocess.call(f"{control} /name Microsoft.PowerOptions", shell=True)


def on_notifications(icon, item):
    global config
    handle_notification_settings(config)
    icon.update_menu()


def on_auto_updates(icon, item):
    global config
    handle_auto_updates(config)
    if config.automatic_updates == True:
        send_notification(
            "Auto Power Saver will now update automatically in the background.",
            config=config,
        )
    icon.update_menu()


def on_release_frequency(icon, item):
    global config
    handle_update_frequency(str(item), config)
    icon.update_menu()


def on_change_timer(icon, item):
    global config
    choice = int(re.search(r"\d+", str(item)).group())
    config.timeout = choice
    config.write_to_config()
    send_notification(
        f"The timeout length was changed to {int(config.timeout)} minutes.",
        config=config,
    )
    icon.update_menu()
