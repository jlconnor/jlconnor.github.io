import os

import mistune
import pygments
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class PicoRenderer(mistune.HTMLRenderer):
    def __init__(self, formatter):
        super().__init__()
        self.formatter = formatter

    def heading(self, text, level, **attrs):
        return f'<h{level} class="h{level}">{text}</h{level}>\n'

    def paragraph(self, text):
        return f'<p class="p">{text}</p>\n'

    def list(self, text, ordered, **attrs):
        tag = "ol" if ordered else "ul"
        return f'<{tag} class="{tag}">{text}</{tag}>\n'

    def list_item(self, text):
        return f'<li class="li">{text}</li>\n'

    def block_code(self, code: str, info=None) -> str:
        language = info.split(None, 1)[0] if info else "text"
        lexer = get_lexer_by_name(language)
        highlighted_code = highlight(code, lexer, self.formatter)
        return f"<pre><code>{highlighted_code}</code></pre>\n"

    def link(self, text: str, url: str, title=None) -> str:
        if url.endswith(".md"):
            url = url[:-3] + ".html"
        if text is None:
            text = url
        if title is not None:
            return f'<a href="{url}" title="{title}">{text}</a>'
        return f'<a href="{url}">{text}</a>'


def convert_markdown_to_html(markdown_content, title):
    formatter = HtmlFormatter()
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


def process_markdown_files(input_directory, output_directory):
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
