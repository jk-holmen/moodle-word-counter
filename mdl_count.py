#!/usr/bin/env python3

import argparse
import html
import os
import re

from bs4 import BeautifulSoup

OUTPUT_FILE_PATH = "./course_out.txt"
CLASSES_TO_STRIP = ["anh-reading"]  # don't include references


def get_input_dir():
    parser = argparse.ArgumentParser(description="Set input and output directories")

    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Path to the input backup file"
    )

    args = parser.parse_args()
    input_file_path = args.input

    if not os.path.isfile(input_file_path):
        raise ValueError(f"Input backup file not found in: {input_file_path}")
    if not os.path.splitext(input_file_path)[-1] == '.mbz':
        raise ValueError(f"File specified does not have an .mbz extension: {input_file_path}")
    
    return input_file_path

def extract_content(file_path, *tags):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "xml")
        content = ""
        for tag in tags:
            content += extract_per_tag(soup, tag)
        return content


# For each xml tag extracted, unescape and parse the html,
# remove divs with skipped classes, then extract only the text
def extract_per_tag(soup, tag_name):
    tags = soup.find_all(tag_name)
    content = ""
    for _, tag_content in enumerate(tags):
        decoded_html = html.unescape(tag_content.text)
        html_soup = BeautifulSoup(decoded_html, "html.parser")

        for cls in CLASSES_TO_STRIP:
            for div in html_soup.find_all("div", class_=cls):
                div.decompose()

        content += html_soup.get_text() + "\n"
    return content


def main():
    input_file_path = get_input_dir()
    content = ""

    for _root, dirs, _files in os.walk(input_file_path + "/activities/"):
        for dir_name in dirs:
            if "page_" in dir_name:
                file_path = input_file_path + "/activities/" + dir_name + "/page.xml"
                print(file_path)
                content += extract_content(file_path, "name", "intro", "content")
            if "book_" in dir_name:
                file_path = input_file_path + "/activities/" + dir_name + "/book.xml"
                print(file_path)
                content += extract_content(
                    file_path, "name", "title", "intro", "content"
                )

    for _root, dirs, _files in os.walk(input_file_path + "/sections/"):
        for dir_name in dirs:
            if "section_" in dir_name:
                file_path = input_file_path + "/sections/" + dir_name + "/section.xml"
                print(file_path)
                content += extract_content(file_path, "name", "summary")

    content = content.replace("\u00a0", "")  # Remove non-breaking spaces
    content = re.sub(r"@@.*", "", content)   # Remove plugin annotations

    with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    main()
