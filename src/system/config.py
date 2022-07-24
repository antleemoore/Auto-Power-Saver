import configparser


class Config:
    def __init__(self, config_path):
        print("Initializing config...")
        self.config_path = config_path
        self.parser = configparser.ConfigParser()
        self.parser.read(config_path)

        try:
            self.parser.get("main", "timeout")
            self.parser.get("main", "disable_notifications")
            self.parser.get("main", "update_frequency")
            self.parser.get("main", "automatic_updates")
            self.timeout = int(self.parser.get("main", "timeout"))
            self.update_frequency = int(self.parser.get("main", "update_frequency"))
            self.automatic_updates = True if self.parser.get("main", "automatic_updates") == "True" else False
            self.disable_notifications = True if self.parser.get("main", "disable_notifications") == "True" else False
        except:
            self.default_values()

    def write_to_config(self):
        print("Writing config to file...")
        try:
            self.parser.set("main", "timeout", str(self.timeout) if str(self.timeout).isdigit() else "3")
            self.parser.set(
                "main",
                "disable_notifications",
                str(self.disable_notifications) if str(self.disable_notifications) in ["True", "False"] else "False",
            )
            self.parser.set(
                "main", "update_frequency", str(self.update_frequency) if str(self.update_frequency).isdigit() else "3"
            )
            self.parser.set(
                "main",
                "automatic_updates",
                str(self.automatic_updates) if str(self.automatic_updates) in ["True", "False"] else "False",
            )
        except:
            self.default_values()
        with open(self.config_path, "w") as f:
            self.parser.write(f)
        print("Config file updated")

    def default_values(self):
        print("Setting config to default values...")
        if not self.parser.has_section("main"):
            self.parser.add_section("main")
        self.parser.set("main", "timeout", "3")
        self.parser.set("main", "disable_notifications", "False")
        self.parser.set("main", "update_frequency", "3")
        self.parser.set("main", "automatic_updates", "False")
        self.timeout = 3
        self.automatic_updates = False
        self.disable_notifications = False
        self.update_frequency = 3
