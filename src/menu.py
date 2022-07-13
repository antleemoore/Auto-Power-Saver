import pystray
from config import Config
from menu_handlers import *
from power_plan import get_plans
import PIL.Image

from system import get_ac_status, resource_path
from update import check_for_updates, get_app_update_versions, on_check_updates

image = PIL.Image.open(resource_path("resources/green_power.jpeg"))
activeplan = "High performance" if get_ac_status().ACLineStatus == 1 else "Power saver"
app_version, update_version = get_app_update_versions()
update = check_for_updates(config)
app_settings = pystray.Menu(
    pystray.MenuItem(
        "Change timeout",
        pystray.Menu(
            pystray.MenuItem(
                "1 minute",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 1,
            ),
            pystray.MenuItem(
                "2 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 2,
            ),
            pystray.MenuItem(
                "3 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 3,
            ),
            pystray.MenuItem(
                "5 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 5,
            ),
            pystray.MenuItem(
                "10 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 10,
            ),
            pystray.MenuItem(
                "15 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 15,
            ),
            pystray.MenuItem(
                "30 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 30,
            ),
            pystray.MenuItem(
                "60 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 60,
            ),
            pystray.MenuItem(
                "120 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout / 60) == 120,
            ),
        ),
    ),
    pystray.MenuItem(
        "Change update frequency",
        pystray.Menu(
            pystray.MenuItem(
                "Major releases",
                on_release_frequency,
                radio=True,
                checked=lambda item: config.update_frequency == 1,
            ),
            pystray.MenuItem(
                "Minor releases",
                on_release_frequency,
                radio=True,
                checked=lambda item: config.update_frequency == 2,
            ),
            pystray.MenuItem(
                "Bug fixes",
                on_release_frequency,
                radio=True,
                checked=lambda item: config.update_frequency == 3,
            ),
        ),
    ),
)
power_settings = pystray.Menu(
    pystray.MenuItem(
        "Create power plan",
        pystray.Menu(
            pystray.MenuItem(
                "High performance",
                on_install,
                checked=lambda item: get_plans().get("High performance") != None,
            ),
            pystray.MenuItem(
                "Power saver",
                on_install,
                checked=lambda item: get_plans().get("Power saver") != None,
            ),
        ),
    ),
    pystray.MenuItem(
        "Delete power plan",
        pystray.Menu(
            pystray.MenuItem("High performance", on_delete),
            pystray.MenuItem("Power saver", on_delete),
        ),
    ),
    pystray.MenuItem("Edit Windows power plan settings", on_win_power_settings),
)
icon = pystray.Icon(
    "Auto Power Saver",
    image,
    title="Auto Power Saver",
    menu=pystray.Menu(
        pystray.MenuItem(f"Version: {app_version}", on_check_updates, enabled=False),
        pystray.MenuItem(
            f"Current power plan: {activeplan}", on_check_updates, enabled=False
        ),
        pystray.MenuItem(
            "Update now", on_check_updates, visible=lambda item: update == True
        ),
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
        pystray.MenuItem("Exit", on_exit),
    ),
)
