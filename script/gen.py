import os

import mistune


def convert_markdown_to_html(markdown_content):
    markdown = mistune.create_markdown()
    html_body = markdown(markdown_content)
    css_url = "https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>jlconnor.github.io</title>
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
                html_content = convert_markdown_to_html(markdown_content)
                with open(output_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)
                print(f"Converted {os.path.join(rel_path, filename)} to HTML.")


def main():
    input_directory = "src"
    output_directory = "."
    process_markdown_files(input_directory, output_directory)


if __name__ == "__main__":
    main()
