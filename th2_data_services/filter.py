class Filter:
    def __init__(self, name: str, values: str or (list, tuple), negative: bool = False, conjunct: bool = False):
        self.name = name

        if isinstance(values, (list, tuple)):
            self.values = map(str, values)
        else:
            self.values = [values]

        self.negative = negative
        self.conjunct = conjunct

    def url(self):
        return (
            f"&filters={self.name}"
            + "".join([f"&{self.name}-values={val}" for val in self.values])
            + f"&{self.name}-negative={self.negative}"
        )
