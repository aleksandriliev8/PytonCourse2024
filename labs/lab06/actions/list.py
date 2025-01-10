"""
list.py:  file for list function
"""

from actions.commands import load_file_data


def my_list() -> None:
    """
    function for printing title and due_date
    """
    notes = load_file_data()
    print("Listing notes...")
    if len(notes) == 0:
        print("Nothing to list.")
    else:
        for title in notes:
            print(
                "- " + title + " (Due: " + notes[title].get("due_date", "None") + ")"
            )  # remove if condition and make it with get function with default value
