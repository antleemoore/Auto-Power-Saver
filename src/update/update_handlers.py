def handle_auto_updates(config):
    config.automatic_updates = True if config.automatic_updates == False else False
    config.write_to_config()


def handle_update_frequency(name, config):
    if name == "Major releases":
        config.update_frequency = 1
    elif name == "Minor releases":
        config.update_frequency = 2
    elif name == "Bug fixes":
        config.update_frequency = 3

    config.write_to_config()
