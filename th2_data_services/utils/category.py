class Category:
    def __init__(self, name: str, get_func):
        self.name: str = name
        self.get_func = get_func

    def __repr__(self):
        return f"Category<{self.name}>"
