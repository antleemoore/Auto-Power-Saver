def handle_auto_updates(config):
    print("Changing automatic updates to " + str(config.automatic_updates))
    config.automatic_updates = True if config.automatic_updates == False else False
    config.write_to_config()


def handle_update_frequency(name, config):
    if name == "Major releases":
        config.update_frequency = 1
    elif name == "Minor releases":
        config.update_frequency = 2
    else:
        config.update_frequency = 3

    print("Changing update frequency to " + name)
    config.write_to_config()
