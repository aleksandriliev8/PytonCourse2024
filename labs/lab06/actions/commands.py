"""
commands.py: file for helper function
"""

import os
import json
from exceptions.MissingDataException import MissingDataException
from exceptions.ExistingTitleException import ExistingTitleException
from exceptions.TitleNotFoundException import TitleNotFoundException


def load_file_data() -> dict:
    """
    function for loading data from file
    """
    notes = None

    if os.path.exists("notes.json"):
        with open("notes.json", "r", encoding="utf-8") as f:
            try:
                notes = json.load(f)
            except json.JSONDecodeError:
                notes = {}
    else:
        notes = {}

    return notes


def validate_for_missing_title(title:str) -> None:
    """
    function for validating empty title
    """
    if title == "":
        raise MissingDataException("title")


def validate_for_missing_content(content:str) -> None:
    """
    function for validating empty content
    """
    if content == "":
        raise MissingDataException("content")


def validate_for_existing_title(title:str, notes:dict) -> None:
    """
    function for validating if title exist in notes 
    """
    if title in notes:
        raise ExistingTitleException(title)


def validete_for_not_existing_title(title:str, notes:dict) -> None:
    """
    function for validating if title does not exist in notes
    """
    if title not in notes:
        raise TitleNotFoundException(title)
