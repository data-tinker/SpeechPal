from processing.pipeline import Pipeline


class PipelineBuilder:
    def __init__(self):
        self._steps = []

    def add_step(self, step):
        self._steps.append(step)
        return self

    def build(self):
        return Pipeline(self._steps)
