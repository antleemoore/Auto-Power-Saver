import pystray

from menu.menu_handlers import (
    on_change_timer,
    on_release_frequency,
    config,
)

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
