import os

import mistune


def main():
    src_directory = "src"
    for root, _, files in os.walk(src_directory):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                with open(md_file_path, "r", encoding="utf-8") as md_file:
                    markdown_content = md_file.read()

                html_content = mistune.html(markdown_content)

                relative_path = os.path.relpath(root, src_directory)
                output_directory = os.path.join(".", relative_path)
                os.makedirs(output_directory, exist_ok=True)

                html_file_name = os.path.splitext(file)[0] + ".html"
                html_file_path = os.path.join(output_directory, html_file_name)
                with open(html_file_path, "w", encoding="utf-8") as html_file:
                    html_file.write("".join(html_content))


if __name__ == "__main__":
    main()
