import configparser
from system.system import get_sys_folder


class Config:
    def __init__(self):
        self.config_path = f'{get_sys_folder("HOME")}\Documents\\auto_power_saver_config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(f'{get_sys_folder("HOME")}\Documents\\auto_power_saver_config.ini')

        try:
            self.config.get("main", "timeout")
            self.config.get("main", "disable_notifications")
            self.config.get("main", "update_frequency")
            self.config.get("main", "automatic_updates")
        except:
            if not self.config.has_section("main"):
                self.config.add_section("main")
            if not self.config.has_option("main", "timeout"):
                self.config.set("main", "timeout", "3")
            if not self.config.has_option("main", "disable_notifications"):
                self.config.set("main", "disable_notifications", "False")
            if not self.config.has_option("main", "update_frequency"):
                self.config.set("main", "update_frequency", "3")
            if not self.config.has_option("main", "automatic_updates"):
                self.config.set("main", "automatic_updates", "False")

        self.timeout = 60 * int(self.config.get("main", "timeout"))
        self.update_frequency = int(self.config.get("main", "update_frequency"))
        self.automatic_updates = True if self.config.get("main", "automatic_updates") == "True" else False
        self.disable_notifications = True if self.config.get("main", "disable_notifications") == "True" else False

    def write_to_config(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)
