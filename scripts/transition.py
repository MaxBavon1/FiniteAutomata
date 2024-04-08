__all__ = ["Transition"]

class Transition:

    def __init__(self, entryState, label : str, endState):
        self.entryState = entryState
        self.label      = label
        self.endState   = endState

    def __str__(self) -> str:
        return f"{self.entryState.state} {self.label} {self.endState.state}"
