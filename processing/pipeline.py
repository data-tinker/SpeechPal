class Pipeline:
    def __init__(self, req_id, steps):
        self._req_id = req_id
        self._steps = steps

    def run(self):
        for step in self._steps:
            step.process()
