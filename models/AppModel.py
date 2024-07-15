class AppModel:
    name: str
    identifier: str
    related_files: list

    def __init__(self, name: str, identifier: str):
        self.name = name
        self.identifier = identifier
        self.relative_identifier = self.__extract_relative_identifier(identifier)

    def __extract_relative_identifier(self, identifier: str):
        name = self.name.replace(' ', '-')

        return identifier.replace(f".{name}", '')
