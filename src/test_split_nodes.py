import unittest
from textnode import (
    TextNode,
    text_type_text,
    split_nodes_image,
    text_type_image,
    text_type_link,
    split_nodes_link,
)


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and more text."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and more text.", text_type_text),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_image_no_images(self):
        text = "This is text with no images."
        node = TextNode(text, text_type_text)
        expected = [node]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_image_mixed_content(self):
        text = "This is text with a ![image](https://example.com/image.jpg) and a link [to a site](https://example.com)."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.jpg"),
            TextNode(" and a link [to a site](https://example.com).", text_type_text),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and more text."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and more text.", text_type_text),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_link_no_links(self):
        text = "This is text with no links."
        node = TextNode(text, text_type_text)
        expected = [node]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_link_mixed_content(self):
        text = "This is text with a ![image](https://example.com/image.jpg) and a link [to a site](https://example.com)."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode(
                "This is text with a ![image](https://example.com/image.jpg) and a link ",
                text_type_text,
            ),
            TextNode("to a site", text_type_link, "https://example.com"),
            TextNode(".", text_type_text),
        ]
        self.assertEqual(split_nodes_link([node]), expected)


if __name__ == "__main__":
    unittest.main()
