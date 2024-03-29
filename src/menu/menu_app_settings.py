import pystray

from menu.menu_handlers import (
    on_auto_updates,
    on_change_timer,
    on_notifications,
    on_release_frequency,
    config,
)

print("Initializing app settings...")
app_settings = pystray.Menu(
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
    pystray.MenuItem(
        "Change timeout",
        pystray.Menu(
            pystray.MenuItem(
                "1 minute",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 1,
            ),
            pystray.MenuItem(
                "2 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 2,
            ),
            pystray.MenuItem(
                "3 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 3,
            ),
            pystray.MenuItem(
                "5 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 5,
            ),
            pystray.MenuItem(
                "10 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 10,
            ),
            pystray.MenuItem(
                "15 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 15,
            ),
            pystray.MenuItem(
                "30 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 30,
            ),
            pystray.MenuItem(
                "60 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 60,
            ),
            pystray.MenuItem(
                "120 minutes",
                on_change_timer,
                radio=True,
                checked=lambda item: (config.timeout) == 120,
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
