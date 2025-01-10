import unittest
import os
import json
from actions.add import add
from exceptions.MissingDataException import MissingDataException
from exceptions.ExistingTitleException import ExistingTitleException


class TestAddFunction(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for testing."""
        self.test_file = "notes.json"
        self.sample_data = {}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.sample_data, f)

    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def load_test_file_data(self):
        """Helper to load data from the test file."""
        with open(self.test_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_add_note_success_with_due_date(self):
        """Test adding a note with both content and due date."""
        add("Test Title", "Test Content", "2025-01-15")

        notes = self.load_test_file_data()
        self.assertIn("Test Title", notes)
        self.assertEqual(
            notes["Test Title"], {"content": "Test Content", "due_date": "2025-01-15"}
        )

    def test_add_note_success_without_due_date(self):
        """Test adding a note with only content."""
        add("Test Title", "Test Content", None)

        notes = self.load_test_file_data()
        self.assertIn("Test Title", notes)
        self.assertEqual(notes["Test Title"], {"content": "Test Content"})

    def test_add_existing_title_raises_exception(self):
        """Test that adding a duplicate title raises an exception."""
        add("Test Title", "Existing Content", "2025-01-15")

        with self.assertRaises(ExistingTitleException):
            add("Test Title", "New Content", "2025-02-01")

    def test_add_missing_content_raises_exception(self):
        """Test that missing content raises an exception."""
        with self.assertRaises(MissingDataException):
            add("Test Title", "", "2025-01-15")

    def test_add_missing_title_raises_exception(self):
        """Test that missing title raises an exception."""
        with self.assertRaises(MissingDataException):
            add("", "Test Content", "2025-01-15")


if __name__ == "__main__":
    unittest.main()
