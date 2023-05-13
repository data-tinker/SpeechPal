from processing.pipeline import Pipeline


class PipelineBuilder:
    def __init__(self, req_id):
        self._req_id = req_id
        self._steps = []

    def add_step(self, step):
        self._steps.append(step)
        return self

    def build(self):
        return Pipeline(self._req_id, self._steps)
