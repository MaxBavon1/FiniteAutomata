from typing import List, Dict
from .state import State

__all__ = ["Automata"]

""" Txt File Format (5 lines):
alphabet
number of states
initial states
terminal states
transitions

example :
a,b,c
4
0,1
2,3
0 a 1,0 c 3,1 b 2
"""



class Automata:

    def __init__(self, alphabet : List[str], states : List[State]):
        self.alphabet : List[str]   = alphabet
        self.states   : List[State] = states
    
    @property
    def num_states(self):
        return len(self.states)

    @property
    def initial_states(self):
        return [state.state for state in self.states if state.isInitial]

    @property
    def final_states(self):
        return [state.state for state in self.states if state.isFinal]

    @classmethod
    def create_from_txt_file(cls, path : str):
        with open(path, 'r') as data:

            alphabet, num_states, initial_states, final_states, transitions = data.readlines()
            
            # --- Alphabet ---
            alphabet = alphabet.replace('\n', '').split(',')
            automata = Automata(alphabet, [])

            # --- States ---
            states = [State(automata, i, False, False) for i in range(int(num_states))]
        
            initial_states = initial_states.split(',')
            final_states = final_states.split(',')

            for state in initial_states:
                states[int(state)].is_initial = True
            for state in final_states:
                states[int(state)].is_final = True

            # --- Transitions ---
            transitions = transitions.split(',')

            for transition in transitions:
                initial, label, final = transition.split(' ')
                states[int(initial)].add_transition(label, final)

        automata.states = states
        return automata

    @classmethod
    def create_from_json_file(cls, path : str):
        pass

    def __str__(self):
        output = "\t  |\t"
        for label in self.alphabet:
            output += f"|{label}\t"
        output += "|\n"
        
        for state in self.states:
            output += str(state)

        return output

    def readWord(self):
        pass