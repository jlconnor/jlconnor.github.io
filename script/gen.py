import os
from typing import Any, Optional

import mistune
import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class PicoRenderer(mistune.HTMLRenderer):
    """
    A custom HTML renderer for Mistune that formats Markdown elements with specific HTML tags and classes.

    Attributes:
        formatter (HtmlFormatter): An instance of HtmlFormatter used for syntax highlighting in code blocks.

    Methods:
        heading(text: str, level: int, **attrs: Any) -> str:
            Renders a heading element with a specified level and text.

        paragraph(text: str) -> str:
            Renders a paragraph element with the given text.

        list(text: str, ordered: bool, **attrs: Any) -> str:
            Renders an ordered or unordered list based on the 'ordered' flag.

        list_item(text: str) -> str:
            Renders a list item element with the given text.

        block_code(code: str, info: Optional[str] = None) -> str:
            Renders a block of code with syntax highlighting based on the specified language.

        link(text: str, url: str, title: Optional[str] = None) -> str:
            Renders a hyperlink element with the given text, URL, and optional title.
    """

    def __init__(self, formatter: HtmlFormatter) -> None:
        super().__init__()
        self.formatter = formatter

    def heading(self, text: str, level: int, **attrs: Any) -> str:
        return f'<h{level} class="h{level}">{text}</h{level}>\n'

    def paragraph(self, text: str) -> str:
        return f'<p class="p">{text}</p>\n'

    def list(self, text: str, ordered: bool, **attrs: Any) -> str:
        tag = "ol" if ordered else "ul"
        return f'<{tag} class="{tag}">{text}</{tag}>\n'

    def list_item(self, text: str) -> str:
        return f'<li class="li">{text}</li>\n'

    def block_code(self, code: str, info: Optional[str] = None) -> str:
        language = info.split(None, 1)[0] if info else "text"
        lexer = get_lexer_by_name(language)
        highlighted_code = highlight(code, lexer, self.formatter)
        return f"<pre><code>{highlighted_code}</code></pre>\n"

    def link(self, text: str, url: str, title: Optional[str] = None) -> str:
        if url.endswith(".md"):
            url = url[:-3] + ".html"
        if text is None:
            text = url
        if title is not None:
            return f'<a href="{url}" title="{title}">{text}</a>'
        return f'<a href="{url}">{text}</a>'


def convert_markdown_to_html(markdown_content: str, title: str) -> str:
    """
    Converts markdown content to HTML format with a specified title.

    Args:
        markdown_content (str): The markdown content to be converted.
        title (str): The title for the HTML document.

    Returns:
        str: The HTML content as a string.
    """
    formatter = HtmlFormatter(style="friendly")
    markdown = mistune.create_markdown(renderer=PicoRenderer(formatter))  # type: ignore
    html_body = markdown(markdown_content)
    # pico.css classes: https://picocss.com/docs/classless
    css_url = "https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="light dark">
        <title>jlconnor.github.io: {title}</title>
        <link rel="stylesheet" href="{css_url}">
        <style>
            {formatter.get_style_defs()}
        </style>
    </head>
    <body>
        <main>
            {html_body}
        </main>
    </body>
    </html>
    """
    return html_content


def process_markdown_files(input_directory: str, output_directory: str) -> None:
    """
    Recursively converts Markdown files in the input directory to HTML files in the output directory.

    Args:
        input_directory (str): Path to the directory containing Markdown files
        output_directory (str): Path to the directory where HTML files will be saved

    Returns:
        None
    """
    for root, dirs, files in os.walk(input_directory):
        rel_path = os.path.relpath(root, input_directory)
        output_subdir = os.path.join(output_directory, rel_path)
        os.makedirs(output_subdir, exist_ok=True)
        for filename in files:
            if filename.endswith(".md"):
                input_path = os.path.join(root, filename)
                output_path = os.path.join(
                    output_subdir, filename.replace(".md", ".html")
                )
                with open(input_path, "r", encoding="utf-8") as md_file:
                    markdown_content = md_file.read()
                title = os.path.splitext(filename)[0]
                html_content = convert_markdown_to_html(markdown_content, title=title)
                with open(output_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)
                print(f"Converted {os.path.join(rel_path, filename)} to HTML.")


def main():
    input_directory = "pages"
    output_directory = "."
    process_markdown_files(input_directory, output_directory)


if __name__ == "__main__":
    main()
