from system.notification import send_notification


def handle_auto_updates(config):
    config.automatic_updates = True if config.automatic_updates == False else False
    config.config.set(
        "main",
        "automatic_updates",
        f'{"True" if config.automatic_updates == True else "False"}',
    )
    if config.automatic_updates == True:
        send_notification(
            "Auto Power Saver will now update automatically in the background.",
            config=config,
        )


def handle_update_frequency(name, config):
    if name == "Major releases":
        config.update_frequency = 1
        config.config.set("main", "update_frequency", str(config.update_frequency))
    elif name == "Minor releases":
        config.update_frequency = 2
        config.config.set("main", "update_frequency", str(config.update_frequency))
    elif name == "Bug fixes":
        config.update_frequency = 3
        config.config.set("main", "update_frequency", str(config.update_frequency))

    config.write_to_config()
