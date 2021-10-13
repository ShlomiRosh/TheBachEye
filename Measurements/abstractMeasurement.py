class AbstractMeasurement:
    def __init__(self):
        self.frame = None

    def run(self, frame, dict_results):
        self.frame = frame

    def __repr__(self):
        raise NotImplementedError
