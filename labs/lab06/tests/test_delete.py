import unittest
import os
import json
from actions.delete import delete
from exceptions.MissingDataException import MissingDataException
from exceptions.TitleNotFoundException import TitleNotFoundException


class TestDeleteFunction(unittest.TestCase):
    def setUp(self):
        """Set up a temporary file for testing."""
        self.test_file = "notes.json"
        self.sample_notes = {
            "Example1": {"content": "1", "due_date": "2025-01-01"},
            "Example2": {"content": "2"},
            "Example3": {"content": "3"}
        }

        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(self.sample_notes, f)

    def tearDown(self):
        """Clean up the temporary file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def load_test_file_data(self):
        """Helper to load data from the test file."""
        with open(self.test_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_delete_existing_note(self):
        """Test deleting a note with existing title"""
        title_to_delete = "Example1"
        delete(title_to_delete)
        notes_after_delete = self.load_test_file_data()
        expected_notes = {"Example2": {"content": "2"}, "Example3": {"content": "3"}}
        self.assertEqual(notes_after_delete, expected_notes)

    def test_delete_non_existing_title(self):
        """Test that non existing title raises an exception."""
        title_to_delete = "non_existing"

        with self.assertRaises(TitleNotFoundException):
            delete(title_to_delete)

    def test_delete_missing_title_raises_exception(self):
        """Test that missing title raises an exception."""
        with self.assertRaises(MissingDataException):
            delete("")


if __name__ == "__main__":
    unittest.main()
