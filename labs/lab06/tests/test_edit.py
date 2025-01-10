import unittest
import os
import json
from actions.edit import edit
from exceptions.MissingDataException import MissingDataException
from exceptions.TitleNotFoundException import TitleNotFoundException

class TestEditFunction(unittest.TestCase):
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

    def load_test_file_data(self):
        """Helper to load data from the test file."""
        with open(self.test_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_edit_with_both_content_and_due_date(self):
        """Test edit a note with both new content and new due_date"""
        edit("Example2", "cont", "11-11-2011")
        notes_after_delete = self.load_test_file_data()
        expected_notes = {
            "Example1": {"content": "1", "due_date": "2025-01-01"},
            "Example2": {"content": "cont", "due_date": "11-11-2011"},
            "Example3": {"content": "3"},
        }
        self.assertEqual(notes_after_delete, expected_notes)

    def test_edit_due_date_with_none(self):
        """Test edit a note with due_date none"""
        edit("Example1", None, "none")
        notes_after_delete = self.load_test_file_data()
        expected_notes = {
            "Example1": {"content": "1"},
            "Example2": {"content": "2"},
            "Example3": {"content": "3"}
        }
        self.assertEqual(notes_after_delete, expected_notes)

    def test_edit_due_date(self):
        """Test edit a note with new due_date"""
        edit("Example3", None, "11-11-2011")
        notes_after_delete = self.load_test_file_data()
        expected_notes = {
            "Example1": {"content": "1", "due_date": "2025-01-01"},
            "Example2": {"content": "2"},
            "Example3": {"content": "3", "due_date": "11-11-2011"}
        }
        self.assertEqual(notes_after_delete, expected_notes)

    def test_edit_content(self):
        """Test edit a note with new content"""
        edit("Example1", "new content", None)
        notes_after_delete = self.load_test_file_data()
        expected_notes = {
            "Example1": {"content": "new content", "due_date": "2025-01-01"},
            "Example2": {"content": "2"},
            "Example3": {"content": "3"}
        }
        self.assertEqual(notes_after_delete, expected_notes)

    def test_edit_without_due_date_and_content(self):
        """Test that non existing title raises an exception."""
        with self.assertRaises(MissingDataException):
            edit("Example1", None, None)

    def test_edit_non_existing_title(self):
        """Test that non existing title raises an exception."""
        with self.assertRaises(TitleNotFoundException):
            edit("non_e", "A", None)

    def test_edit_missing_title_raises_exception(self):
        """Test that missing title raises an exception."""
        with self.assertRaises(MissingDataException):
            edit("", "Test Content", "2025-01-15")

if __name__ == "__main__":
    unittest.main()
