import pystray
from menu.menu_handlers import *
import PIL.Image

from system.system import get_ac_status, resource_path
from update.update import check_for_updates, get_app_update_versions, on_check_updates
from menu.menu_app_settings import app_settings
from menu.menu_power_settings import power_settings
from menu.menu_additional_features import additional_features

image = PIL.Image.open(resource_path("resources/images/green_power.jpeg"))
activeplan = "High performance" if get_ac_status().ACLineStatus == 1 else "Power saver"
app_version, update_version = get_app_update_versions()
update = check_for_updates(config)

icon = pystray.Icon(
    "Auto Power Saver",
    image,
    title="Auto Power Saver",
    menu=pystray.Menu(
        pystray.MenuItem(f"Version: {app_version}", on_check_updates, enabled=False),
        pystray.MenuItem(f"Current power plan: {activeplan}", on_check_updates, enabled=False),
        pystray.MenuItem("Update now", on_check_updates, visible=lambda item: update == True),
        pystray.MenuItem(
            "Disable notifications",
            on_notifications,
            checked=lambda item: config.disable_notifications == True,
        ),
        pystray.MenuItem(
            "Automatic updates",
            on_auto_updates,
            checked=lambda item: config.automatic_updates == True,
        ),
        pystray.MenuItem("Power settings", power_settings),
        pystray.MenuItem("App settings", app_settings),
        pystray.MenuItem("Additional features", additional_features),
        pystray.MenuItem("Exit", on_exit),
    ),
)
