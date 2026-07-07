"""
File: news_service.py
Purpose: Fetch and cache AquaVision environmental news.

Author: AquaVision AI
Project: AquaVision AI Backend
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import requests

from app.core.config import settings
from app.core.logging import logger

CACHE_FILE = Path("cache/news_cache.json")


class NewsService:

    NEWS_URL = "https://api.currentsapi.services/v1/search"

    MAX_ARTICLES = 10

    SEARCH_QUERIES = [
        "water pollution",
        "river pollution",
        "drinking water",
        "groundwater",
        "water conservation",
        "wastewater treatment",
        "climate change",
        "flood",
        "drought",
        "lake pollution",
    ]

    KEYWORDS = [
        "water",
        "river",
        "lake",
        "groundwater",
        "pollution",
        "environment",
        "climate",
        "wastewater",
        "drinking water",
        "conservation",
        "ocean",
        "sea",
        "rain",
        "flood",
        "drought",
        "dam",
        "reservoir",
        "wetland",
    ]

    INDIA_KEYWORDS = [
        "india",
        "indian",
        "ganga",
        "yamuna",
        "godavari",
        "krishna",
        "cauvery",
        "narmada",
        "cpcb",
        "jal",
        "monsoon",
    ]

    def _load_cache(self):

        if not CACHE_FILE.exists():
            return None

        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_cache(self, articles):

        data = {
            "last_updated": datetime.now().isoformat(),
            "provider": "Currents API",
            "total_articles": len(articles),
            "articles": articles,
        }

        with open(CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def _cache_valid(self, cache):

        if not cache:
            return False

        last_updated = cache.get("last_updated")

        if not last_updated:
            return False

        try:
            last = datetime.fromisoformat(last_updated)
        except ValueError:
            return False

        return (
            datetime.now() - last
        ) < timedelta(seconds=settings.NEWS_CACHE_DURATION)

    def fetch_news(self):

        logger.info("Checking news cache...")

        cache = self._load_cache()

        if self._cache_valid(cache):

            logger.info("Returning cached news.")

            return cache["articles"]

        query = random.choice(self.SEARCH_QUERIES)

        logger.info(f"Fetching news using query: {query}")

        params = {
            "apiKey": settings.NEWS_API_KEY,
            "keywords": query,
            "language": "en",
            "page_size": 15,
        }

        response = requests.get(
            self.NEWS_URL,
            params=params,
            timeout=15,
        )
        
        print(response.status_code)
        print(response.text)

        response.raise_for_status()

        data = response.json()

        indian_news = []
        global_news = []

        seen_urls = set()

        for article in data.get("news", []):

            title = article.get("title") or ""
            description = article.get("description") or ""

            text = f"{title} {description}".lower()

            if not any(word in text for word in self.KEYWORDS):
                continue

            url = article.get("url")

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            item = {
                "title": title,
                "description": description,
                "image": article.get("image"),
                "url": url,
                "source": article.get("author") or "Unknown",
                "published": article.get("published"),
            }

            if any(word in text for word in self.INDIA_KEYWORDS):
                indian_news.append(item)
            else:
                global_news.append(item)

        articles = indian_news + global_news

        articles = articles[: self.MAX_ARTICLES]

        self._save_cache(articles)

        logger.info(
            f"Cached {len(articles)} environmental news articles."
        )

        return articles
    
    
#


news_service = NewsService()