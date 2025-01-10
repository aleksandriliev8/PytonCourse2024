class MissingDataException(Exception):

    def __init__(self, data):
        super().__init__(f"Note with empty {data}")
