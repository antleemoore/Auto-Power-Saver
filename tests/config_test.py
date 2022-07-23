import datetime
import os
import unittest
import sys

sys.path.append("./src/system")
from config import Config

ct = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat() + "Z"
ct = ct.replace(":", "_")
ct = ct.replace(".", "_")

# Test Config class
class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.config_path = f"./tests/output/config_test__{ct}.ini"
        self.config = Config(self.config_path)

    def test_config_init(self):
        self.assertEqual(self.config.config_path, self.config_path)
        self.assertEqual(self.config.parser.get("main", "timeout"), "3")
        self.assertEqual(self.config.parser.get("main", "disable_notifications"), "False")
        self.assertEqual(self.config.parser.get("main", "update_frequency"), "3")
        self.assertEqual(self.config.parser.get("main", "automatic_updates"), "False")
        self.assertEqual(self.config.timeout, 3)
        self.assertEqual(self.config.automatic_updates, False)
        self.assertEqual(self.config.disable_notifications, False)
        self.assertEqual(self.config.update_frequency, 3)

    def test_config_write_to_config(self):
        self.config.write_to_config()

        self.assertEqual(self.config.parser.get("main", "timeout"), "3")
        self.assertEqual(self.config.parser.get("main", "disable_notifications"), "False")
        self.assertEqual(self.config.parser.get("main", "update_frequency"), "3")
        self.assertEqual(self.config.parser.get("main", "automatic_updates"), "False")
        self.assertEqual(self.config.timeout, 3)
        self.assertEqual(self.config.automatic_updates, False)
        self.assertEqual(self.config.disable_notifications, False)
        self.assertEqual(self.config.update_frequency, 3)

    def test_config_default_values(self):
        self.config.timeout = 120
        self.config.write_to_config()

        self.config.default_values()

        self.assertEqual(self.config.parser.get("main", "timeout"), "3")

    def tearDown(self):
        try:
            os.remove(self.config_path)
        except FileNotFoundError:
            pass
        self.config = None
        self.config_path = None


if __name__ == "__main__":
    if not os.path.exists("tests/output"):
        os.makedirs("tests/output")
    unittest.main(verbosity=2)
