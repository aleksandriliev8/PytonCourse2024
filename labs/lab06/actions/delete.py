"""
delete.py: file for delete function
"""

import json
from actions.commands import load_file_data
from actions.commands import validate_for_missing_title
from actions.commands import validete_for_not_existing_title


def delete(title:str) -> None:
    """
    function for deleting notes
    """
    notes = load_file_data()
    validate_for_missing_title(title)
    validete_for_not_existing_title(title, notes)
    del notes[title]
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f)
    print("Deleted.")
