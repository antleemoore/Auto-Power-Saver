import re
import subprocess
from config import Config
from notification import handle_notification_settings, send_notification
from power_plan import delete_power_plan, install_power_plan
from update import handle_auto_updates, handle_update_frequency

control = "%SystemRoot%\system32\control.exe"
config = Config()
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
    icon.update_menu()


def on_release_frequency(icon, item):
    global config
    handle_update_frequency(str(item), config)
    icon.update_menu()


def on_change_timer(icon, item):
    global config
    choice = int(re.search(r"\d+", str(item)).group())
    config.timeout = 60 * choice
    config.config.set("main", "timeout", str(int(config.timeout / 60)))
    config.write_to_config()
    send_notification(
        f"The timeout length was changed to {int(config.timeout / 60)} minutes.",
        config=config,
    )
    icon.update_menu()
