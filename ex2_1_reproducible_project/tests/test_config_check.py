import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config_check import missing_settings

class ConfigTests(unittest.TestCase):
    def test_all_present(self): self.assertEqual(missing_settings({"APP_MODE":"demo","SERVICE_TOKEN":"dummy"}), [])
    def test_missing_token_names_only(self): self.assertEqual(missing_settings({"APP_MODE":"demo","SERVICE_TOKEN":""}), ["SERVICE_TOKEN"])
    def test_blank_mode(self): self.assertEqual(missing_settings({"APP_MODE":"  ","SERVICE_TOKEN":"dummy"}), ["APP_MODE"])
if __name__ == "__main__": unittest.main()
