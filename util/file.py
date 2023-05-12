from typing import NamedTuple


class File(NamedTuple):
    path: str
    name: str
    extension: str

    def full_path(self):
        return f'{self.path}/{self.name}.{self.extension}'
