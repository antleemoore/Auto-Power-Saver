import tkinter as tk
from tkinter import tix
from tkinter.tix import Balloon
from system.file_search import menu_item_run_search
from menu.menu_handlers import (
    config,
    on_auto_updates,
    on_change_timer,
    on_delete,
    on_exit,
    on_install,
    on_notifications,
    on_release_frequency,
    on_win_power_settings,
)
from system.system import resource_path


def update(icon, item, setting):
    if setting == "Disable notifications":
        on_notifications(icon, None)
    elif setting == "Automatic updates":
        on_auto_updates(icon, None)
    elif setting == "Change timer":
        on_change_timer(icon, item)
    elif setting == "Change update frequency":
        on_release_frequency(icon, item)


def close_application(window, icon):
    window.destroy()
    on_exit(icon, None)


# function to open a tkinter window
def open_window(icon, item):
    # set window
    window = tix.Tk()
    window.title("Auto Power Saver")
    window.geometry("265x530")
    window.minsize(265, 530)
    window.iconbitmap(default=resource_path("resources/images/green_power.ico"))
    window.resizable(False, False)

    disable_notifications = tk.Checkbutton(
        window,
        text="Disable notifications",
        onvalue=True,
        offvalue=False,
        variable=config.disable_notifications,
        command=lambda: update(icon, setting="Disable notifications"),
    )
    disable_notifications.select() if config.disable_notifications else disable_notifications.deselect()

    automatic_updates = tk.Checkbutton(
        window,
        text="Automatic updates",
        onvalue=True,
        offvalue=False,
        variable=config.automatic_updates,
        command=lambda: update(icon, setting="Automatic updates"),
    )
    automatic_updates.select() if config.automatic_updates else automatic_updates.deselect()

    timeouts = ["1", "2", "3", "5", "10", "15", "30", "60", "120"]
    timeout_options = tk.StringVar(window)
    timeout_options.set(config.timeout)
    timeout_menu = tk.OptionMenu(
        window,
        timeout_options,
        *timeouts,
        command=lambda x: update(icon=icon, item=x, setting="Change timer"),
    )
    # add label to timeout_menu
    timeout_label = tk.Label(window, text="Timeout:", justify=tk.RIGHT)

    update_freqs = ["Major releases", "Minor releases", "Big fixes"]
    update_options = tk.StringVar(window)

    update_options.set(update_freqs[int(config.update_frequency) - 1])
    update_freq_menu = tk.OptionMenu(
        window,
        update_options,
        *update_freqs,
        command=lambda x: update(icon=icon, item=x, setting="Change update frequency"),
    )
    # add label to timeout_menu
    update_label = tk.Label(window, text="Update frequency:", justify=tk.RIGHT)
    app_settings_label = tk.Label(window, text="Application Settings", font="Segoe 12 bold", pady=10)
    power_settings_label = tk.Label(window, text="Power Plan Settings", font="Segoe 12 bold", pady=10)
    create_power_label = tk.Label(window, text="Install", font="Segoe 10 bold", pady=10)
    delete_power_label = tk.Label(window, text="Delete", font="Segoe 10 bold", pady=10)
    additional_feature_label = tk.Label(window, text="Additional Features", font="Segoe 12 bold", pady=10)

    open_windows_power_settings_button = tk.Button(
        window,
        text="Open Windows Power Settings",
        command=lambda: on_win_power_settings(None, None),
    )
    install_high_perf_power_button = tk.Button(
        window,
        text="Install High performance Power Plan",
        command=lambda: on_install(icon, "High performance"),
    )
    install_power_saver_power_button = tk.Button(
        window,
        text="Install Power saver Power Plan",
        command=lambda: on_install(icon, "Power saver"),
    )
    delete_high_perf_power_button = tk.Button(
        window,
        text="Delete High performance Power Plan",
        command=lambda: on_delete(icon, "High performance"),
    )
    delete_power_saver_power_button = tk.Button(
        window,
        text="Delete Power saver Power Plan",
        command=lambda: on_delete(icon, "Power saver"),
    )
    deep_file_search_button = tk.Button(
        window,
        text="Run deep file search",
        command=lambda: menu_item_run_search(),
    )
    exit_button = tk.Button(
        window,
        text="Close application",
        command=lambda: close_application(window, icon),
    )
    search_tip = Balloon(window)
    search_tip.bind_widget(
        deep_file_search_button,
        balloonmsg="Searches for matching file names in the selected computer drive",
    )
    update_tip = Balloon(window)
    update_tip.bind_widget(
        update_freq_menu,
        balloonmsg="Major releases:\tLeast frequent updates.\nMinor releases:\tMore frequent updates.\nBig fixes:\t\tMost frequent updates.",
    )
    first_row = 0

    app_settings_label.grid(row=first_row, column=0, columnspan=2)
    disable_notifications.grid(row=first_row + 1, column=0, columnspan=1, sticky="w")
    automatic_updates.grid(row=first_row + 1, column=1, sticky="w")
    timeout_label.grid(row=first_row + 2, column=0)
    timeout_menu.grid(row=first_row + 2, column=1, sticky="w")
    update_label.grid(row=first_row + 3, column=0)
    update_freq_menu.grid(row=first_row + 3, column=1, sticky="w")
    power_settings_label.grid(row=first_row + 4, column=0, columnspan=2)
    open_windows_power_settings_button.grid(row=first_row + 5, column=0, columnspan=2)
    create_power_label.grid(row=first_row + 6, column=0, columnspan=2)
    install_high_perf_power_button.grid(row=first_row + 7, column=0, columnspan=2)
    tk.Label(window, text="", font="Segoe 1 bold", padx=0, pady=0).grid(row=first_row + 8, column=0, sticky="w")
    install_power_saver_power_button.grid(row=first_row + 9, column=0, columnspan=2)
    delete_power_label.grid(row=first_row + 10, column=0, columnspan=2)
    delete_high_perf_power_button.grid(row=first_row + 11, column=0, columnspan=2)
    tk.Label(window, text="", font="Segoe 1 bold", padx=0, pady=0).grid(row=first_row + 12, column=0, sticky="w")
    delete_power_saver_power_button.grid(row=first_row + 13, column=0, columnspan=2)
    additional_feature_label.grid(row=first_row + 14, column=0, columnspan=2)
    deep_file_search_button.grid(row=first_row + 15, column=0, columnspan=2)
    tk.Label(window, text="", font="Segoe 1 bold", pady=10).grid(row=first_row + 16, column=0, sticky="w")
    exit_button.grid(row=first_row + 17, column=0, columnspan=2)
    icon.visible = False
    # run the window
    window.mainloop()
    icon.visible = True
