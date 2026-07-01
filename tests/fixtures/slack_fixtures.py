import httpx

from aws import get_secret

SLACK_TOKEN = get_secret("support-analyzer/slack-bot-token")
SLACK_CHANNEL = "parlez-support"
HEADERS = {"Authorization": f"Bearer {SLACK_TOKEN}"}


def post_slack_message(text: str) -> dict:
    resp = httpx.post(
        "https://slack.com/api/chat.postMessage",
        headers=HEADERS,
        json={"channel": SLACK_CHANNEL, "text": text},
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack postMessage failed: {data}")
    return {"ts": data["ts"], "channel": data["channel"]}


def delete_slack_message(channel: str, ts: str) -> None:
    resp = httpx.post(
        "https://slack.com/api/chat.delete",
        headers=HEADERS,
        json={"channel": channel, "ts": ts},
    )
    resp.raise_for_status()
