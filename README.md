# WeChat Message Helper

**A small Python script for sending a configured WeChat template message.**

`Python` · `WeChat API` · `Legacy script`

## What it sends

Weather, an anniversary day count, birthday reminders, and a daily quote to the recipients configured by the operator.

## Before running

You need a compatible WeChat account/template and your own app credentials, template ID, and recipient IDs. Copy `config.example.json` to `config.txt` and fill in your own values. `config.txt` is ignored by Git. Alternatively, provide the entire JSON configuration in the `WECHAT_CONFIG_JSON` environment variable; it takes precedence over the file.

| Setting | Purpose |
| --- | --- |
| `app_id`, `app_secret` | WeChat API credentials |
| `template_id` | Message template |
| `user` | Recipient ID list |
| `province`, `city` | Weather location |
| `love_date` | Anniversary date in `YYYY-MM-DD` format |

```bash
python -m pip install -r requirements.txt
```

After reviewing the configuration and recipients, `python main.py` sends the message. It is not a preview command.

## Limitations

This is a legacy implementation with pinned dependencies and external weather/quote services. Configuration accepts JSON or the original Python literal format without executing code. Weather responses are decoded as JSON. Do not commit real credentials or recipient information.

The sending workflow is opt-in: set the repository secret `WECHAT_CONFIG_JSON` and the Actions variable `WECHAT_SEND_ENABLED=true` only when you intend to send messages on its schedule. Pushes run parser tests only. Test safely with `python -m unittest discover -s tests`; those tests make no network requests and send no messages.

If credentials were previously committed, removing the current file does not erase Git history. Replace those credentials with fresh ones before enabling delivery.

`main.py` contains the sending flow; `cityinfo.py` contains the weather-location lookup.
