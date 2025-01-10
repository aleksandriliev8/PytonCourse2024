"""
main.py: Command-line Note-Taking Application.
Supports actions: add, view, delete, list, edit.
"""

from actions.add import add
from actions.view import view
from actions.delete import delete
from actions.list import my_list
from actions.edit import edit  # import edit
from exceptions.TitleNotFoundException import TitleNotFoundException
from exceptions.MissingDataException import MissingDataException
from exceptions.ExistingTitleException import ExistingTitleException


try:
    import argparse

    parser = argparse.ArgumentParser(description="Command-line Note-Taking Application")
    parser.add_argument(
        "action",
        choices=["add", "view", "delete", "list", "edit"],
        help="What do you want to do?",
    )  # add edit in choices

    parser.add_argument("--title", help="Title of the note")
    parser.add_argument("--content", help="Content of the note (only for `add` action)")
    parser.add_argument("--due-date", help="Optional due date (only for `add` action)")
    args = parser.parse_args()

    if args.action == "add":
        if args.title is None:
            print("Need title.")
        elif args.content is None:
            print("Needs content.")
        else:
            add(args.title, args.content, args.due_date)
    elif args.action == "view":
        view(args.title)
    elif args.action == "delete":
        delete(args.title)
    elif args.action == "list":
        my_list()
    # add edit in factory
    elif args.action == "edit":
        edit(args.title, args.content, args.due_date)
    else:
        print("Invalid action.")
except TitleNotFoundException as e:
    print(e)
except MissingDataException as e:
    print(e)
except ExistingTitleException as e:
    print(e)
