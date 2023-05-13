from typing import NamedTuple


class File(NamedTuple):
    path: str
    id: str
    name: str
    extension: str

    def full_path(self):
        return f'{self.path}/{self.id}/{self.name}.{self.extension}'

    def path_without_extension(self):
        return f'{self.path}/{self.id}/{self.name}'
