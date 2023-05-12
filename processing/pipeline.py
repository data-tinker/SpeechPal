class Pipeline:
    def __init__(self, steps):
        self._steps = steps

    def run(self):
        for step in self._steps:
            step.process()
