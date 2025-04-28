import argparse
import os
import shutil
from typing import Any

import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <meta name="description" content="Personal website of Jason Connor - Software Engineer">
    <meta name="author" content="Jason Connor">
    <meta property="og:title" content="Jason Connor - {title}">
    <meta property="og:description" content="Personal website of Jason Connor - Software Engineer">
    <meta property="og:image" content="assets/profile.jpg">
    <title>Jason Connor - {title}</title>
    <link rel="stylesheet" href="{css_url}">
    <style>
        /* Custom styles */
        :root {{
            --typography-spacing-vertical: 1.5rem;
            --font-family: system-ui, -apple-system, "Segoe UI", "Roboto", sans-serif;
        }}
        body > header,
        body > footer {{
            padding: var(--spacing);
            background: var(--card-background-color);
        }}
        body > header {{
            border-bottom: 1px solid var(--card-border-color);
        }}
        body > footer {{
            border-top: 1px solid var(--card-border-color);
            text-align: center;
        }}
        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        nav a {{
            text-decoration: none;
            color: var(--h1-color);
        }}
        pre {{
            padding: 0.5rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }}
        code {{
            font-family: ui-monospace, "Cascadia Code", "Source Code Pro", Menlo, Consolas, monospace;
        }}
        {pygments_style}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Jason Connor</a>
        </nav>
    </header>
    <main>
        {nav_link}
        {html_body}
        {nav_link}
    </main>
    <footer>
        <small>© 2025 Jason Connor • Built with <a href="https://picocss.com">Pico CSS</a></small>
    </footer>
</body>
</html>
"""


class PicoRenderer(mistune.HTMLRenderer):
    """
    A custom HTML renderer for Mistune that formats Markdown elements with specific HTML tags and classes.

    Attributes:
        formatter (HtmlFormatter): An instance of HtmlFormatter used for syntax highlighting in code blocks.
    """

    def __init__(self, formatter: HtmlFormatter) -> None:
        super().__init__()
        self.formatter = formatter

    def heading(self, text: str, level: int, **attrs: Any) -> str:
        return f'<h{level} class="h{level}">{text}</h{level}>\n'

    def paragraph(self, text: str) -> str:
        return f'<p class="p" style="max-width: 70ch">{text}</p>\n'

    def list(self, text: str, ordered: bool, **attrs: Any) -> str:
        tag = "ol" if ordered else "ul"
        return f'<{tag} class="{tag}">{text}</{tag}>\n'

    def list_item(self, text: str) -> str:
        return f'<li class="li">{text}</li>\n'

    def block_code(self, code: str, info: str | None = None) -> str:
        language = info.split(None, 1)[0] if info else "text"
        lexer = get_lexer_by_name(language)
        highlighted_code = highlight(code, lexer, self.formatter)

        return (
            f'<pre><code class="language-{language}">{highlighted_code}</code></pre>\n'
        )

    def link(self, text: str | None, url: str, title: str | None = None) -> str:
        # Handle both .md files and internal links without extension
        if url.endswith(".md"):
            url = url[:-3] + ".html"
        elif not url.startswith(("http://", "https://", "#", "/")) and "." not in url:
            url = url + ".html"

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
    nav_link = ""
    if title != "index":
        nav_link = '<p class="p" style="max-width: 70ch"><a href="index.html">← Return to homepage</a></p>'

    # pygments built-in styles: https://pygments.org/styles/
    formatter = HtmlFormatter(style="friendly")
    markdown = mistune.create_markdown(renderer=PicoRenderer(formatter))  # type: ignore
    html_body = markdown(markdown_content)

    # pico.css classes: https://picocss.com/docs/classless
    css_url = "https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css"
    pygments_style = formatter.get_style_defs()
    html_content = _HTML_TEMPLATE.format(
        title=title,
        html_body=html_body,
        css_url=css_url,
        pygments_style=pygments_style,
        nav_link=nav_link,
    )

    return html_content


def process_markdown_files(input_directory: str, output_directory: str) -> None:
    """
    Recursively converts Markdown files in the input directory to HTML files in the output directory.
    Copies non-Markdown files as-is.

    Args:
        input_directory (str): Path to the directory containing Markdown files
        output_directory (str): Path to the directory where HTML files will be saved

    Returns:
        None
    """
    for root, _, files in os.walk(input_directory):
        relative_path = os.path.relpath(root, input_directory)
        output_dir = os.path.join(output_directory, relative_path)
        os.makedirs(output_dir, exist_ok=True)

        for f in files:
            input_path = os.path.join(root, f)
            output_path = os.path.join(output_dir, f)

            if f.endswith(".md"):
                with open(input_path, "r", encoding="utf-8") as md_file:
                    md_content = md_file.read()

                if not md_content.strip():
                    print(f"Skipping empty file: {os.path.join(relative_path, f)}")
                    continue

                output_path = output_path.removesuffix(".md") + ".html"
                title = os.path.splitext(f)[0]
                html_content = convert_markdown_to_html(md_content, title=title)

                with open(output_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)

                print(f"Converted {os.path.join(relative_path, f)} to HTML.")

            else:
                shutil.copy2(input_path, output_path)
                print(f"Copied {os.path.join(relative_path, f)} to {output_path}.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to HTML and copy non-Markdown files."
    )
    parser.add_argument(
        "input_directory",
        type=str,
        help="The input directory containing Markdown files.",
    )
    parser.add_argument(
        "output_directory", type=str, help="The output directory to save HTML files."
    )

    args = parser.parse_args()
    process_markdown_files(args.input_directory, args.output_directory)


if __name__ == "__main__":
    main()
