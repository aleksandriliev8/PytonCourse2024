"""
view.py: file for view function
"""

from actions.commands import load_file_data
from actions.commands import validate_for_missing_title
from actions.commands import validete_for_not_existing_title


def view(title:str) -> None:
    """
    function for adding new notes
    """
    notes = load_file_data()
    validate_for_missing_title(title)
    validete_for_not_existing_title(title, notes)
    print(title)
    print("---")
    print(notes[title]["content"])
    print("---")
    if notes[title].get("due_date", False):  # edit this get
        print("Due:" + notes[title]["due_date"])
    else:
        print("No due date.")
