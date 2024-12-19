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

                html_file_name = os.path.splitext(file)[0] + ".html"
                with open(html_file_name, "w", encoding="utf-8") as html_file:
                    html_file.write("".join(html_content))


if __name__ == "__main__":
    main()
