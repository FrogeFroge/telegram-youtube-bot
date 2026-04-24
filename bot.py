import feedparser
import time
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
YOUTUBE_FEED = os.environ.get("YOUTUBE_FEED")

if not BOT_TOKEN or not CHAT_ID or not YOUTUBE_FEED:
    print("❌ Ошибка: не заданы переменные окружения")
    exit(1)

seen_videos = set()

def send_video_notification(title, url):
    text = f"🎬 НОВОЕ ВИДЕО!\n\n<b>{title}</b>\n\n👇 Смотреть:"
    keyboard = {
        "inline_keyboard": [
            [{"text": "▶️ Смотреть на YouTube", "url": url}]
        ]
    }
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text,
                "reply_markup": keyboard,
                "parse_mode": "HTML"
            },
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ Отправлено: {title}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Исключение: {e}")

def check_youtube():
    try:
        feed = feedparser.parse(YOUTUBE_FEED)
        for entry in feed.entries[:5]:
            if entry.link not in seen_videos:
                seen_videos.add(entry.link)
                send_video_notification(entry.title, entry.link)
    except Exception as e:
        print(f"❌ Ошибка проверки YouTube: {e}")

if __name__ == "__main__":
    print("🚀 Бот запущен. Жду новых видео...")
    while True:
        check_youtube()
        time.sleep(3600)
