"""Parse local configuration and weather data without executing input."""

import ast
import json
import os
from pathlib import Path


def parse_config(text):
    # Preserve legacy Python-literal files with comments, as well as JSON secrets.
    try:
        config = json.loads(text)
    except json.JSONDecodeError:
        config = ast.literal_eval(text)
    if not isinstance(config, dict):
        raise ValueError("Configuration must be an object")
    for key in ("app_id", "app_secret", "template_id", "province", "city", "love_date"):
        if not isinstance(config.get(key), str) or not config[key].strip():
            raise ValueError("Missing required configuration field: " + key)
    users = config.get("user")
    if not isinstance(users, list) or not users or not all(isinstance(user, str) and user.strip() for user in users):
        raise ValueError("Configure at least one recipient ID")
    return config


def load_config(path="config.txt"):
    secret = os.environ.get("WECHAT_CONFIG_JSON")
    return parse_config(secret if secret is not None else Path(path).read_text(encoding="utf-8"))


def parse_weather_response(text):
    # The endpoint wraps JSON in a JavaScript assignment. Decode only its JSON value.
    payload = text.lstrip()
    if not payload.startswith("{"):
        prefix, separator, payload = payload.partition("=")
        if not separator or not prefix.strip():
            raise ValueError("Weather response has no JSON assignment")
    data, _ = json.JSONDecoder().raw_decode(payload.lstrip())
    if not isinstance(data, dict) or not isinstance(data.get("weatherinfo"), dict):
        raise ValueError("Weather response has no weatherinfo object")
    return data
