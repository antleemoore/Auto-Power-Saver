import pystray
from menu.menu_handlers import config, on_exit
import PIL.Image

from system.system import get_ac_status, resource_path
from ui.index import open_window
from update.update import check_for_updates, get_app_update_versions, on_check_updates
from menu.menu_app_settings import app_settings
from menu.menu_power_settings import power_settings
from menu.menu_additional_features import additional_features

print("Initializing menu icon...")
image = PIL.Image.open(resource_path("resources/images/green_power.jpeg"))
print()
activeplan = "High performance" if get_ac_status().ACLineStatus == 1 else "Power saver"
app_version, update_version = get_app_update_versions()
update = check_for_updates(config)
print()

icon = pystray.Icon(
    "Auto Power Saver",
    image,
    title="Auto Power Saver",
    menu=pystray.Menu(
        pystray.MenuItem(f"Version: {app_version}", open_window, enabled=False),
        pystray.MenuItem(f"Open", open_window, default=True),
        pystray.MenuItem(f"Current power plan: {activeplan}", on_check_updates, visible=False, enabled=False),
        pystray.MenuItem("Update now", on_check_updates, visible=lambda item: update == True),
        pystray.MenuItem("Power plan settings", power_settings, visible=False),
        pystray.MenuItem("Application settings", app_settings, visible=False),
        pystray.MenuItem("Additional features", additional_features, visible=False),
        pystray.MenuItem("Exit", on_exit),
    ),
)
