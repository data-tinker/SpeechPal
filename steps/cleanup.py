import os

from steps.step import AbstractStep


class CleanUpStep(AbstractStep):
    def __init__(self, files):
        self._files = files

    def process(self):
        for file in self._files:
            if os.path.exists(file.full_path()):
                os.remove(file.full_path())
