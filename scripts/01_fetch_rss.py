import json
import re
from datetime import datetime, timedelta, time
from pathlib import Path
from zoneinfo import ZoneInfo

import feedparser
from dateutil import parser as dtparser

KST = ZoneInfo("Asia/Seoul")

# Google News RSS (비즈니스 토픽)
FEEDS = [
    "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ko&gl=KR&ceid=KR:ko",
]

OUT_DIR = Path("docs/data")
ARCHIVE_DIR = OUT_DIR / "archive"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def split_google_title(title: str):
    # Google News RSS는 흔히 "제목 - 언론사" 형태
    if " - " in title:
        a, b = title.rsplit(" - ", 1)
        if 2 <= len(b) <= 40:
            return normalize_space(a), normalize_space(b)
    return normalize_space(title), None

def parse_dt(s: str):
    dt = dtparser.parse(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.astimezone(KST)

def main():
    now = datetime.now(KST)
    ydate = (now - timedelta(days=1)).date()

    start = datetime.combine(ydate, time.min, tzinfo=KST)
    end = datetime.combine(ydate, time.max, tzinfo=KST)

    items = []
    seen_links = set()

    for url in FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            raw_title = e.get("title", "")
            title, source_hint = split_google_title(raw_title)

            link = e.get("link")
            if not link or link in seen_links:
                continue

            published = e.get("published") or e.get("updated")
            if not published:
                continue

            try:
                dt = parse_dt(published)
            except Exception:
                continue

            if not (start <= dt <= end):
                continue

            source = source_hint or "Unknown"

            items.append({
                "title": title,
                "source": source,
                "link": link,
                "published_kst": dt.isoformat(),
            })
            seen_links.add(link)

    out = {
        "date_kst": str(ydate),
        "generated_at_kst": now.isoformat(),
        "items": sorted(items, key=lambda x: x["published_kst"], reverse=True),
    }

    (OUT_DIR / "raw.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    (ARCHIVE_DIR / f"{ydate}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()