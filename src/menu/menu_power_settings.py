import pystray
from menu.menu_handlers import on_delete, on_install, on_win_power_settings

from system.power_plan import get_plans

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
