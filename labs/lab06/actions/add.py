"""
add.py: file for add function
"""

import json
from actions.commands import load_file_data
from actions.commands import validate_for_missing_title
from actions.commands import validate_for_missing_content
from actions.commands import validate_for_existing_title


def add(title:str, content:str, due_date:str) -> None:
    """
    function for adding new notes
    """
    notes = load_file_data()
    validate_for_missing_title(title)
    validate_for_missing_content(content)
    validate_for_existing_title(title, notes)
    if due_date:
        notes[title] = {"content": content, "due_date": due_date}
    else:
        notes[title] = {
            "content": content,
        }
    with open("notes.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(notes))
    print("Added new note", title)
