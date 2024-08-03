import re
import unittest


def extract_title(markdown):
    match = re.search(r"^# (.+)", markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    else:
        raise Exception("No h1 header found in the markdown")


class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("# Hello World"), "Hello World")
        self.assertEqual(extract_title("Some text\n# Title\nMore text"), "Title")

    def test_extract_title_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("No header here")


if __name__ == "__main__":
    unittest.main()
