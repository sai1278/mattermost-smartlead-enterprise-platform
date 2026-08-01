from tmmp_integrations_mattermost.markdown import MarkdownBuilder


def test_markdown_builder_simple():
    builder = MarkdownBuilder()
    text = builder.bold("Header:").text("This is").italic("important").build()
    assert "**Header:** This is *important*" in text


def test_markdown_heading_and_code():
    text = (
        MarkdownBuilder()
        .heading("Title", level=1)
        .newline()
        .code_block("print('hello')", language="python")
        .build()
    )
    assert "# Title" in text
    assert "```python\nprint('hello')\n```" in text


def test_markdown_mention_and_link():
    text = (
        MarkdownBuilder()
        .mention("@alice")
        .text("visit")
        .link("Docs", "https://docs.mattermost.com")
        .build()
    )
    assert "@alice visit [Docs](https://docs.mattermost.com)" in text
