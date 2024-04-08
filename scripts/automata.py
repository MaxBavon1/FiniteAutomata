from typing import List, Dict
from .transition import Transition
from .state import State

__all__ = ["Automata"]

""" Txt File Format (5 lines):
alphabet
number of states
initial stats
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

    @classmethod
    def create_from_txt_file(cls, path : str):
        data = open(path, 'r')

        alphabet, num_states, initial_states, final_states, transitions = data.readlines()
        
        alphabet = alphabet.replace('\n', '').split(',')

        states = [State(i, False, False) for i in range(int(num_states))]
        initial_states = initial_states.split(',')
        final_states = final_states.split(',')

        for state in initial_states:
            states[int(state)].isInitial = True
        for state in final_states:
            states[int(state)].isFinal = True

        
        transitions = transitions.split(',')
        for transition in transitions:
            initial, label, final = transition.split(' ')
            transition = Transition(states[int(initial)], label, states[int(final)])
            states[int(initial)].addTransition(transition)
        
        return Automata(alphabet, states)

    @classmethod
    def create_from_json_file(cls, path : str):
        pass

    def __str__(self):
        output = f"Alphabet: {self.alphabet}\n"
        
        for state in self.states:
            output += f"\t{state}\n"

        return output

    def readWord(self):
        pass