"""
edit.py: file for edit function
"""

# add new function
import json
from exceptions.MissingDataException import MissingDataException
from actions.commands import load_file_data
from actions.commands import validate_for_missing_title
from actions.commands import validete_for_not_existing_title


def edit(title:str, content:str, due_date:str) -> None:
    """
    function for editing notes
    """

    notes = load_file_data()
    validate_for_missing_title(title)
    validete_for_not_existing_title(title, notes)
    if not due_date and not content:
        raise MissingDataException(
            "content or due date provided - no changes made to the note."
        )
    if content:
        notes[title]["content"] = content
    if due_date:
        if due_date.lower() == "none":
            notes[title].pop("due_date", None)
        else:
            notes[title]["due_date"] = due_date
    with open("notes.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(notes))
    print("Note successfully edited.")
