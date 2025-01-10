import unittest
import os
import json
from actions.view import view
from exceptions.MissingDataException import MissingDataException
from exceptions.TitleNotFoundException import TitleNotFoundException


class TestViewFunction(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for testing."""
        self.test_file = "notes.json"
        self.sample_notes = {
            "Example1": {"content": "1", "due_date": "2025-01-01"},
            "Example2": {"content": "2"},
            "Example3": {"content": "3"},
        }

        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.sample_notes, f)

    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_view_with_valid_title_with_due_date(self):
        """Print title, content and due date from given title"""
        view("Example1")

    def test_view_with_valid_title_without_due_date(self):
        """Print title, content and due date from given title"""
        view("Example2")

    def test_view_non_existing_title(self):
        """Test that non existing title raises an exception."""

        with self.assertRaises(TitleNotFoundException):
            view("non_existing")

    def test_view_missing_title_raises_exception(self):
        """Test that missing title raises an exception."""
        with self.assertRaises(MissingDataException):
            view("")


if __name__ == "__main__":
    unittest.main()
