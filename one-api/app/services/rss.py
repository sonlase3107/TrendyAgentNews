import re
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import certifi

from app.core.db import get_connection
from app.core.exceptions import RSSException
from app.schemas.calculation import ArticleItem
from app.schemas.rss import FetchRSSRequest, TopicFetchError, TopicRecord

_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


class RSSService:
    """Business logic for RSS feed operations."""

    _SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

    def list_topics(self) -> list[TopicRecord]:
        """Return all active topics stored in the database.

        Queries the ``topics`` table for rows where ``is_active = 1`` and
        maps each row to a :class:`TopicRecord`.
        """
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, name, category, is_active, created_at, url, domain "
                "FROM topics WHERE is_active = 1"
            ).fetchall()
        return [TopicRecord(**dict(row)) for row in rows]

    def fetch_rss(
        self, payload: FetchRSSRequest
    ) -> tuple[list[ArticleItem], list[TopicFetchError]]:
        """Fetch and parse RSS feeds for the requested topics.

        Resolves each ``topic_id`` to a URL via the database, then fetches
        and parses the feed.  Failures are captured per-topic so that
        processing continues for the remaining topics (partial-success policy).

        Returns a tuple ``(merged_items, per_topic_errors)`` where
        ``merged_items`` is sorted by ``pub_date`` descending.
        """
        items: list[ArticleItem] = []
        errors: list[TopicFetchError] = []

        for topic_ref in payload.topics:
            try:
                url = self._resolve_url(topic_ref.topic_id)
                fetched = self._fetch_and_parse(url, source_override=topic_ref.topic_name)
                items.extend(fetched)
            except RSSException as exc:
                errors.append(
                    TopicFetchError(
                        topic_id=topic_ref.topic_id,
                        topic_name=topic_ref.topic_name,
                        error=exc.message,
                    )
                )

        items.sort(
            key=lambda a: a.pub_date if a.pub_date is not None else _EPOCH,
            reverse=True,
        )
        return items, errors

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_url(self, topic_id: str) -> str:
        """Look up the RSS URL for the given ``topic_id`` from the database.

        Raises :class:`RSSException` when the topic is not found or inactive.
        """
        with get_connection() as conn:
            row = conn.execute(
                "SELECT url, is_active FROM topics WHERE id = ?", (topic_id,)
            ).fetchone()

        if row is None:
            raise RSSException(f"Topic '{topic_id}' not found")
        if not row["is_active"]:
            raise RSSException(f"Topic '{topic_id}' is inactive")
        return row["url"]

    def _fetch_and_parse(self, url: str, source_override: str) -> list[ArticleItem]:
        """Fetch raw RSS XML from ``url`` and parse all ``<item>`` elements.

        Raises :class:`RSSException` on network or XML parse failures.
        """
        try:
            with urllib.request.urlopen(
                url, timeout=10, context=self._SSL_CONTEXT
            ) as response:
                raw_bytes = response.read()
        except Exception as exc:
            raise RSSException(f"Failed to fetch feed: {exc}") from exc

        try:    
            raw_xml = raw_bytes.decode("utf-8", errors="replace")
            root = ET.fromstring(raw_xml)
        except ET.ParseError as exc:
            raise RSSException(f"Failed to parse feed XML: {exc}") from exc

        channel = root if root.tag == "channel" else root.find("channel")
        if channel is None:
            raise RSSException("No <channel> element found in the feed")

        source_name = source_override or (channel.findtext("title") or "").strip()
        return [self._map_item(item, source_name) for item in channel.findall("item")]

    def _map_item(self, item: ET.Element, source_name: str) -> ArticleItem:
        """Map a single ``<item>`` element to an :class:`ArticleItem`."""
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or "").strip() or None
        raw_desc = item.findtext("description") or ""
        description = self._strip_html(raw_desc).strip() or None
        pub_date = self._parse_date(item.findtext("pubDate"))
        media_count = len(item.findall("enclosure"))

        return ArticleItem(
            title=title,
            url=url,
            pub_date=pub_date,
            description=description,
            source_name=source_name or None,
            guid=guid,
            media_count=media_count,
        )

    @staticmethod
    def _strip_html(text: str) -> str:
        """Remove HTML tags from a string."""
        return re.sub(r"<[^>]+>", "", text)

    @staticmethod
    def _parse_date(raw: str | None) -> datetime | None:
        """Parse an RFC-2822 date string; return ``None`` on failure."""
        if not raw:
            return None
        try:
            return parsedate_to_datetime(raw.strip())
        except Exception:
            return None
