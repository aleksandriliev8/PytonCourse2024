import unittest
import os
import json
from actions.add import add
from actions.list import my_list


class TestListFunction(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for testing."""
        self.test_file = "notes.json"
        self.sample_notes = {}

        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.sample_notes, f)

    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_list_with_empty_notes(self):
        """Print nothing to list"""
        my_list()

    def test_list_notes(self):
        """Print all elements title and due date in file."""
        add("Title", "Content", None)
        add("Title1", "Content", "11-11-2011")
        my_list()


if __name__ == "__main__":
    unittest.main()
