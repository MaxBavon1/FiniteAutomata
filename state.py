from typing import List, Dict, Tuple

__all__ = ["State"]


""" Transition Format:
Dict = {label1 : list of states, label2 : list of states, ...}
example:
{a : [1, 2], b : [3, 4]}
"""

class State:

    def __init__(self, automata, state : int, is_initial : bool, is_final : bool) -> None:
        self.automata                       = automata
        self.state       : int              = state
        self.transitions : Dict[str : List] = {label : [] for label in automata.alphabet}
        self.is_initial  : bool             = is_initial
        self.is_final    : bool             = is_final
    
    def get_transitions_list(self) -> List[Tuple]:
        transitions = []

        for label, final_states in self.transitions.items():
            for final_state in final_states:
                transitions.append((self, label, final_state))
        
        return transitions
    
    def union(self, *states): # For determinization<w
        for state in states:
            for label in state.transitions:
                self.transitions[label] += state.transitions[label]
    
    def add_transition(self, label : str, state) -> None:
        if label in self.transitions:
            self.transitions[label].append(state)
        else:
            print("Label not in alphabet !")

    def __str__(self):
        output = "\t"
        output += "I" if self.is_initial else " "
        output += "F" if self.is_final else " "
        output += f"|{self.state}\t"
        
        for states in self.transitions.values():
            output += '|'
            
            for i in range(len(states)):
                output += f"{states[i].state}"
                if i != len(states) - 1:
                    output += ','

            output += '\t'

        output += "|\n"
        return output