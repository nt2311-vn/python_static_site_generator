import unittest

from textnode import (
    TextNode,
    text_to_textnodes,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_italic,
    text_type_link,
    text_type_image,
)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text with no markdown."
        expected = [TextNode(text, text_type_text)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_only_bold(self):
        text = "This is **bold** text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text.", text_type_text),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_only_italic(self):
        text = "This is *italic* text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text.", text_type_text),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_only_code(self):
        text = "This is `code` text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" text.", text_type_text),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_only_link(self):
        text = "This is a [link](https://example.com) text."
        expected = [
            TextNode("This is a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(" text.", text_type_text),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_text_to_textnodes_only_image(self):
        text = "This is an ![image](https://example.com/image.jpg) text."
        expected = [
            TextNode("This is an ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.jpg"),
            TextNode(" text.", text_type_text),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()
