import re
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

from app.core.exceptions import CalculationException
from app.schemas.calculation import ArticleItem, CalculationRequest, CalculationResult


class CalculationService:
    """Business logic for arithmetic calculation endpoints."""

    def evaluate(self, payload: CalculationRequest) -> CalculationResult:
        """Evaluate arithmetic operation based on the request payload."""
        if payload.operation == "add":
            result = payload.left + payload.right
        elif payload.operation == "subtract":
            result = payload.left - payload.right
        elif payload.operation == "multiply":
            result = payload.left * payload.right
        else:
            if payload.right == 0:
                raise CalculationException("Division by zero is not allowed")
            result = payload.left / payload.right

        return CalculationResult(operation=payload.operation, value=result)

    def extract_articles(self, raw_data: str) -> list[ArticleItem]:
        """Parse a raw XML string into a list of ArticleItem objects.

        Raises CalculationException when the input cannot be parsed as valid XML.
        """
        channel, source_name = self._parse_channel(raw_data.strip())
        return [self._map_item(item, source_name) for item in channel.findall("item")]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_channel(self, xml_text: str) -> tuple[ET.Element, str]:
        """Parse the XML and return the <channel> element and its title string."""
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            raise CalculationException(f"Invalid XML input: {exc}") from exc

        channel = root if root.tag == "channel" else root.find("channel")
        if channel is None:
            raise CalculationException("No <channel> element found in the provided XML")

        source_name = (channel.findtext("title") or "").strip()
        return channel, source_name

    def _map_item(self, item: ET.Element, source_name: str) -> ArticleItem:
        """Map a single <item> element to an ArticleItem model."""
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
    def _parse_date(raw: str | None):
        """Parse an RFC-2822 date string; return None on failure."""
        if not raw:
            return None
        try:
            return parsedate_to_datetime(raw.strip())
        except Exception:
            return None
    

