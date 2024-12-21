import os

import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class PicoRenderer(mistune.HTMLRenderer):
    def heading(self, text, level, **attrs):
        return f'<h{level} class="h{level}">{text}</h{level}>\n'

    def paragraph(self, text):
        return f'<p class="p">{text}</p>\n'

    def list(self, text, ordered, **attrs):
        tag = "ol" if ordered else "ul"
        return f'<{tag} class="{tag}">{text}</{tag}>\n'

    def list_item(self, text):
        return f'<li class="li">{text}</li>\n'

    def block_quote(self, text, language="python"):
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter()
        highlighted_text = highlight(text, lexer, formatter)
        return f'<blockquote class="blockquote">{highlighted_text}</blockquote>\n'


def convert_markdown_to_html(markdown_content, title):
    # markdown = mistune.create_markdown(renderer=PicoRenderer())
    markdown = mistune.create_markdown()
    html_body = markdown(markdown_content)
    css_url = "https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="light dark">
        <title>jlconnor.github.io: {title}</title>
        <link rel="stylesheet" href="{css_url}">
    </head>
    <body>
        {html_body}
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
    input_directory = "src"
    output_directory = "."
    process_markdown_files(input_directory, output_directory)


if __name__ == "__main__":
    main()
