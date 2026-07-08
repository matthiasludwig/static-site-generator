import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        # Test case 1: Title present
        markdown = "# This is a title\nThis is some content."
        self.assertEqual(extract_title(markdown), "This is a title")

        # Test case 2: No title present
        markdown = "This is some content without a title."
        self.assertEqual(extract_title(markdown), "")

        # Test case 3: Title with leading spaces
        markdown = "   # This is a title with leading spaces\nThis is some content."
        self.assertEqual(extract_title(markdown), "This is a title with leading spaces")

        # Test case 4: Multiple titles, should return the first one
        markdown = "# First Title\n# Second Title\nThis is some content."
        self.assertEqual(extract_title(markdown), "First Title")