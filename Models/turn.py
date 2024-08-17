class Turn:

    def __init__(self):
        self.command1 = None
        self.command2 = None

    def can_start(self):
        return self.command1 is not None and self.command2 is not None
            