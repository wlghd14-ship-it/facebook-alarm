import feedparser
import requests
import os
import json

# 👇 바로 이 아래부분의 주소를 메모장에 있는 진짜 주소로 바꿔주세요!
# 주의: 주소 양옆의 작은 따옴표(' ')는 지워지면 안 됩니다.
RSS_FEEDS = {
    '첫번째페이지이름': 'https://rss.app/feeds/TEHYiRj5GWMzYu5A.xml',
    '두번째페이지이름': 'https://rss.app/feeds/HZUpYR881Q3mMls8.xml'
}

BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TRACKING_FILE = "last_links.json"

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

def main():
    last_links = {}
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, "r", encoding="utf-8") as f:
            try:
                last_links = json.load(f)
            except json.JSONDecodeError:
                last_links = {}

    for page_name, rss_url in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue

        latest_entry = feed.entries[0]
        latest_link = latest_entry.link
        latest_title = latest_entry.title

        last_sent_link = last_links.get(page_name, "")

        if latest_link != last_sent_link:
            msg = f"[{page_name}] 새 글 알림!\n\n{latest_title}\n{latest_link}"
            send_telegram_msg(msg)
            last_links[page_name] = latest_link 

    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(last_links, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
