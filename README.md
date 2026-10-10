# WeChat Message Helper

**A small Python script for sending a configured WeChat template message.**

`Python` · `WeChat API` · `Legacy script`

## What it sends

Weather, an anniversary day count, birthday reminders, and a daily quote to the recipients configured by the operator.

## Before running

You need a compatible WeChat account/template and your own app credentials, template ID, and recipient IDs. The script reads `config.txt` from the current working directory.

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

This is a legacy implementation with pinned dependencies and external weather/quote services. It uses `eval()` for configuration and a weather response; replace that parsing before treating it as a reusable service. Do not commit real credentials or recipient information in `config.txt`.

`main.py` contains the sending flow; `cityinfo.py` contains the weather-location lookup.
