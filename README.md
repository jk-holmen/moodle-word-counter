# moodle-word-counter
A command-line tool to get an approximate word count for a Moodle course.

## Features

* Outputs a total word count for Moodle sections and activities (`page.xml`, `book.xml`, `section.xml`)
* Optionally writes all extracted text to `course_out.txt` to a directory of your choice

Note: the output text is not in order!

## Requirements

* **Python ≥ 3.12**
* Dependencies:

  * `lxml`
  * `beautifulsoup4`

If you're using `uv`, dependencies will be handled automatically.

## Running the script

```sh
uv run mwc.py -i /abs/path/to/backup
```

Optionally, an output directory can be specified with the `-o` or `--ouput` flags:

```sh
uv run mwc.py -i /abs/path/to/backup/ -o /abs/path/to/output/
```

### Notes

* Paths must be **absolute**.
* The backup directory must already be extracted (rename .mbz to .gzip and extract it)
* The script will only extract from the following:
  * `activities/` with `page_*/page.xml` or `book_*/book.xml`
  * `sections/` with `section_*/section.xml`

## Example

```sh
uv run mwc.py -i /home/me/course_backup -o /home/me/output
```

Output:

```
/home/me/course_backup/activities/book_193/book.xml
/home/me/course_backup/activities/book_205/book.xml
/home/me/course_backup/activities/book_221/book.xml
/home/me/course_backup/activities/page_10/page.xml
/home/me/course_backup/activities/page_11/page.xml
/home/me/course_backup/activities/page_12/page.xml
/home/me/course_backup/activities/page_15/page.xml
Word count: 15342
```

