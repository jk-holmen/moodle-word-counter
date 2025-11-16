#!/usr/bin/env
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["lxml", "bs4"]
# ///

import argparse
import html
import os
import re
from pathlib import Path

from bs4 import BeautifulSoup

OUTPUT_FILE_NAME = "course_out.txt"
CLASSES_TO_STRIP = ["anh-reading"]  # don't include references


class WordCounter:
    def __init__(self):
        args = self.get_args()
        self.course = Course(args.input, args.output)

    def get_args(self):
        parser = argparse.ArgumentParser(
            description="Get the word count of a Moodle course from a backup file"
        )

        parser.add_argument(
            "-i",
            "--input",
            type=str,
            required=True,
            help="Declare a path to the input backup file",
        )

        parser.add_argument(
            "-o",
            "--output",
            type=str,
            required=False,
            help="Declare an output directory in which the extracted course text will be saved",
        )
        return parser.parse_args()

    def run(self):
        self.course.extract_content()

        word_count = len(self.course.content.split())
        print(f"Word count: {word_count}")


class Course:
    def __init__(self, input_path, output_path=None):
        self.input_path = Path(input_path)
        self._validate_path(self.input_path)

        if output_path is not None:
            self.output_path = Path(output_path)
            self._validate_path(self.output_path)
        else:
            self.output_path = None

        self.content = None

    def _validate_path(self, path):
        if not path.is_absolute():
            raise ValueError(f"Given file path is not absolute: {path}")
        # if not os.path.isfile(self.input_path):
        #    raise ValueError(f"Input backup file not found in: {self.input_path}")
        # if not os.path.splitext(self.input_path)[-1] == ".mbz":
        #    raise ValueError(
        #        f"File specified does not have an .mbz extension: {self.input_path}"
        #    )

    def extract_content(self):
        path = self.input_path

        content = ""

        for _root, dirs, _files in os.walk(path / "activities"):
            for dir_name in dirs:
                if "page_" in dir_name:
                    file_path = path / "activities" / dir_name / "page.xml"
                    print(file_path)
                    content += self._extract_from_file(
                        file_path, "name", "intro", "content"
                    )
                if "book_" in dir_name:
                    file_path = path / "activities" / dir_name / "book.xml"
                    print(file_path)
                    content += self._extract_from_file(
                        file_path, "name", "title", "intro", "content"
                    )

        for _root, dirs, _files in os.walk(path / "sections"):
            for dir_name in dirs:
                if "section_" in dir_name:
                    file_path = path / "sections" / dir_name / "section.xml"
                    print(file_path)
                    content += self._extract_from_file(file_path, "name", "summary")

        content = content.replace("\u00a0", "")  # Remove non-breaking spaces
        content = re.sub(r"@@.*", "", content)  # Remove plugin annotations

        self.content = content

        if self.output_path is not None:
            self._output_content()

    def _extract_from_file(self, file_path, *tags):
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "xml")
            content = ""
            for tag in tags:
                content += self._extract_per_tag(soup, tag)
            return content

    # For each xml tag extracted, unescape and parse the html,
    # remove divs with skipped classes, then extract only the text
    def _extract_per_tag(self, soup, tag_name):
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

    def _output_content(self):
        with open(self.output_path / OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
            file.write(self.content)


def main():
    counter = WordCounter()
    counter.run()


if __name__ == "__main__":
    main()
