import datetime
import os
import unittest
import sys

sys.path.append("./src/update")
from update_handlers import handle_auto_updates, handle_update_frequency

sys.path.append("./src/system")
from config import Config

ct = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z"
ct = ct.replace(":", "_")
ct = ct.replace(".", "_")


class UpdateHandlersTest(unittest.TestCase):
    def setUp(self):
        self.config_path = f"./tests/output/update_handlers_test__{ct}.ini"
        self.config = Config(self.config_path)
        self.config.disable_notifications = True
        self.config.update_frequency = 0
        self.config.write_to_config()

    def test_handle_auto_updates(self):
        initial_value = self.config.update_frequency

        handle_auto_updates(self.config)

        self.assertEqual(initial_value, False)
        self.assertEqual(self.config.parser.get("main", "automatic_updates"), "True")

    def test_handle_update_frequency(self):
        initial_value = self.config.update_frequency

        handle_update_frequency("Major releases", self.config)

        self.assertEqual(initial_value, 0)
        self.assertEqual(self.config.parser.get("main", "update_frequency"), "1")

        initial_value = self.config.update_frequency

        handle_update_frequency("Minor releases", self.config)

        self.assertEqual(initial_value, 1)
        self.assertEqual(self.config.parser.get("main", "update_frequency"), "2")

        initial_value = self.config.update_frequency

        handle_update_frequency("Bug fixes", self.config)

        self.assertEqual(initial_value, 2)
        self.assertEqual(self.config.parser.get("main", "update_frequency"), "3")


if __name__ == "__main__":
    if not os.path.exists("tests/output"):
        os.makedirs("tests/output")
    unittest.main(verbosity=2)
