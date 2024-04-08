from typing import List
from .transition import Transition

__all__ = ["State"]

class State:

    def __init__(self, state : int, isInitial : bool, isFinal : bool) -> None:
        self.state       : int             = state
        self.transitions : List[Transition] = []
        self.isInitial   : bool             = isInitial
        self.isFinal     : bool             = isFinal
    
    def addTransition(self, transition : Transition) -> None:
        self.transitions.append(transition)
    
    def __str__(self) -> str:
        output = f"State: {self.state} Initial: {self.isInitial} Final : {self.isFinal}\n"

        for transition in self.transitions:
            output += f"\t{transition}\n"

        return output