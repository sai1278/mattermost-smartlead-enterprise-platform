"""Interactive Attachment Builder for Mattermost Messages."""

from __future__ import annotations

from typing import Any


class InteractiveAttachmentBuilder:
    """Fluent Builder for Mattermost Slack-compatible interactive message attachments."""

    def __init__(self) -> None:
        self._fallback: str = ""
        self._color: str = "#0080FF"
        self._text: str = ""
        self._title: str = ""
        self._title_link: str = ""
        self._fields: list[dict[str, Any]] = []
        self._actions: list[dict[str, Any]] = []

    def title(self, title: str, link: str = "") -> InteractiveAttachmentBuilder:
        self._title = title
        self._title_link = link
        return self

    def text(self, text: str) -> InteractiveAttachmentBuilder:
        self._text = text
        return self

    def color(self, hex_color: str) -> InteractiveAttachmentBuilder:
        self._color = hex_color
        return self

    def fallback(self, fallback_text: str) -> InteractiveAttachmentBuilder:
        self._fallback = fallback_text
        return self

    def add_field(self, title: str, value: str, short: bool = True) -> InteractiveAttachmentBuilder:
        self._fields.append({"title": title, "value": value, "short": short})
        return self

    def add_button(self, id: str, name: str, integration_url: str) -> InteractiveAttachmentBuilder:
        self._actions.append(
            {
                "id": id,
                "name": name,
                "type": "button",
                "integration": {"url": integration_url},
            }
        )
        return self

    def build(self) -> dict[str, Any]:
        attachment: dict[str, Any] = {
            "fallback": self._fallback or self._title or self._text,
            "color": self._color,
            "text": self._text,
            "title": self._title,
        }
        if self._title_link:
            attachment["title_link"] = self._title_link
        if self._fields:
            attachment["fields"] = self._fields
        if self._actions:
            attachment["actions"] = self._actions
        return attachment
