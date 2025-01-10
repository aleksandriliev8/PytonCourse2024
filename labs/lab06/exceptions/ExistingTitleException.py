class ExistingTitleException(Exception):

    def __init__(self, title):
        super().__init__(f"Note with title '{title}' already exist.")
