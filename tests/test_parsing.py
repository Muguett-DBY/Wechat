import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from parsing import load_config, parse_config, parse_weather_response


class ParsingTests(unittest.TestCase):
    def setUp(self):
        self.example = Path("config.example.json").read_text(encoding="utf-8")

    def test_accepts_json_and_legacy_literals_with_comments(self):
        expected = json.loads(self.example)
        self.assertEqual(parse_config(self.example), expected)
        self.assertEqual(parse_config("# local config\n" + repr(expected)), expected)

    def test_rejects_executable_configuration(self):
        with self.assertRaises(ValueError):
            parse_config("__import__('os').getcwd()")

    def test_rejects_invalid_recipient_and_missing_credentials(self):
        for replacement in ({"user": "not-a-list"}, {"user": []}, {"app_secret": ""}):
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                parse_config(json.dumps({**json.loads(self.example), **replacement}))

    def test_environment_config_takes_precedence_over_local_file(self):
        with patch.dict(os.environ, {"WECHAT_CONFIG_JSON": self.example}):
            self.assertEqual(load_config("does-not-exist.txt"), json.loads(self.example))

    def test_local_file_fallback(self):
        with TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            path = Path(directory) / "config.txt"
            path.write_text(self.example, encoding="utf-8")
            self.assertEqual(load_config(path), json.loads(self.example))

    def test_weather_assignment_handles_json_values_and_delimiters(self):
        weather = {"weatherinfo": {"weather": "sunny;clear=good", "extra": None, "ok": True}}
        for text in (json.dumps(weather), "var cityDZ = " + json.dumps(weather) + "; var ignored = 1;"):
            self.assertEqual(parse_weather_response(text), weather)

    def test_weather_rejects_code_and_missing_data(self):
        for text in ("var x = __import__('os').getcwd();", "var x = {};", "not-json"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_weather_response(text)


if __name__ == "__main__":
    unittest.main()
