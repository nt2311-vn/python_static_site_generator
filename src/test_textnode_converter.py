import unittest
from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node(self):
        text_node = TextNode(text="Just text", text_type="text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(tag=None, value="Just text"))

    def test_bold_node(self):
        text_node = TextNode(text="Bold text", text_type="bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(tag="b", value="Bold text"))

    def test_italic_node(self):
        text_node = TextNode(text="Italic text", text_type="italic")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(tag="i", value="Italic text"))

    def test_code_node(self):
        text_node = TextNode(text="Code text", text_type="code")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node, LeafNode(tag="code", value="Code text"))

    def test_link_node(self):
        text_node = TextNode(
            text="Link text", text_type="link", url="https://example.com"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node,
            LeafNode(tag="a", value="Link text", props={"href": "https://example.com"}),
        )

    def test_image_node(self):
        text_node = TextNode(
            text="Alt text", text_type="image", url="https://example.com/image.jpg"
        )
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            html_node,
            LeafNode(
                tag="img",
                value="",
                props={"src": "https://example.com/image.jpg", "alt": "Alt text"},
            ),
        )

    def test_unknown_text_type(self):
        text_node = TextNode(text="Unknown text", text_type="unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_link_node_without_url(self):
        text_node = TextNode(text="Link text", text_type="link")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_image_node_without_url(self):
        text_node = TextNode(text="Alt text", text_type="image")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def setUp(self):
        self.text_type_text = "text"
        self.text_type_bold = "bold"
        self.text_type_italic = "italic"
        self.text_type_code = "code"
        self.text_type_link = "link"
        self.text_type_image = "image"

    def test_split_code_node(self):
        node = TextNode("This is text with a `code block` word", self.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", self.text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", self.text_type_text),
            TextNode("code block", self.text_type_code),
            TextNode(" word", self.text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_bold_node(self):
        node = TextNode(
            "This is text with a **bold phrase** in the middle", self.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", self.text_type_bold)
        expected_nodes = [
            TextNode("This is text with a ", self.text_type_text),
            TextNode("bold phrase", self.text_type_bold),
            TextNode(" in the middle", self.text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_italic_node(self):
        node = TextNode(
            "This is text with an *italic phrase* in the middle", self.text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "*", self.text_type_italic)
        expected_nodes = [
            TextNode("This is text with an ", self.text_type_text),
            TextNode("italic phrase", self.text_type_italic),
            TextNode(" in the middle", self.text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_unmatched_delimiter(self):
        node = TextNode(
            "This is text with an unmatched *italic phrase in the middle",
            self.text_type_text,
        )
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", self.text_type_italic)


if __name__ == "__main__":
    unittest.main()
