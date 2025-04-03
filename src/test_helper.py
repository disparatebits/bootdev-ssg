import unittest

from src.helper import extract_title


class TestHelperFunctions(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        result = extract_title(md)
        self.assertEqual(result, "Hello")

    def test_extract_title_raises_exception(self):
        md = " Hello"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_multiple_headers(self):
        md = '''
# Hello
# This should return Hello        
'''
        result = extract_title(md)
        self.assertEqual(result, "Hello")