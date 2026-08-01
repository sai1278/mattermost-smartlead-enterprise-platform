"""Fluent Builder for Mattermost Markdown Formatted Strings."""

from __future__ import annotations


class MarkdownBuilder:
    """Fluent API for constructing Mattermost markdown formatted text."""

    def __init__(self) -> None:
        self._parts: list[str] = []

    def text(self, content: str) -> MarkdownBuilder:
        self._parts.append(content)
        return self

    def bold(self, content: str) -> MarkdownBuilder:
        self._parts.append(f"**{content}**")
        return self

    def italic(self, content: str) -> MarkdownBuilder:
        self._parts.append(f"*{content}*")
        return self

    def code(self, content: str) -> MarkdownBuilder:
        self._parts.append(f"`{content}`")
        return self

    def code_block(self, code: str, language: str = "") -> MarkdownBuilder:
        self._parts.append(f"```{language}\n{code}\n```")
        return self

    def heading(self, title: str, level: int = 1) -> MarkdownBuilder:
        hashes = "#" * max(1, min(level, 6))
        self._parts.append(f"{hashes} {title}")
        return self

    def bullet(self, item: str) -> MarkdownBuilder:
        self._parts.append(f"- {item}")
        return self

    def mention(self, username: str) -> MarkdownBuilder:
        user = username.lstrip("@")
        self._parts.append(f"@{user}")
        return self

    def link(self, label: str, url: str) -> MarkdownBuilder:
        self._parts.append(f"[{label}]({url})")
        return self

    def newline(self) -> MarkdownBuilder:
        self._parts.append("\n")
        return self

    def build(self) -> str:
        return " ".join(self._parts).replace(" \n ", "\n").replace("\n ", "\n")
