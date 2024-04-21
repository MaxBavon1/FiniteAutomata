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
        return [state for state in self.states if state.is_initial]

    @property
    def final_states(self):
        return [state for state in self.states if state.is_final]

    @property
    def transitions(self):
        """
        List of tuples (initial state, label, final state)
        """
        transitions = []

        for state in self.states:
            transitions += state.get_transitions_list()

        return transitions

    def __str__(self):
        output = "\t  |\t"
        for label in self.alphabet:
            output += f"|{label}\t"
        output += "|\n"
        
        for state in self.states:
            output += str(state)

        return output

    @classmethod
    def create_from_txt_file(cls, path : str) -> 'Automata':
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
                states[int(initial)].add_transition(label, states[int(final)])

        automata.states = states
        return automata

    @classmethod
    def create_from_json_file(cls, path : str):
        pass


    def is_standard(self) -> bool:
        single_state = len(self.initial_states) == 1

        entry_transitions = [transition for transition in self.transitions if transition[2] in self.initial_states]

        return single_state and not(entry_transitions)

    def standardize(self):
        if not self.is_standard():
            new_state = State(self, self.num_states, True, False)
            for state in self.initial_states:

                for label, final_states in state.transitions.items():
                    for final_state in final_states:
                        new_state.add_transition(label, final_state)

                state.is_initial = False
            self.states.append(new_state)


    def is_complete(self) -> bool:
        for state in self.states:
            for final_states in state.transitions.values():
                if not final_states:
                    return False
        return True

    def completion(self):
        if not self.is_complete():
            new_state = State(self, self.num_states, False, False)

            for label in self.alphabet: # Recursive Transitions to P
                new_state.add_transition(label, new_state)

            for state in self.states:   # Fill Transitions to P
                for label in state.transitions:
                    if not state.transitions[label]:
                        state.add_transition(label, new_state)

            self.states.append(new_state)

    def is_deterministic(self) -> bool:
        for state in self.states:
            if any(len(final_states) > 1 for final_states in state.transitions.values()):
                return False

        return len(self.initial_states) == 1
    
    # def determinize(self):
    #     # ouin ouin quoicoubeh c'est dur

    def complementarily(self):
        for state in self.states:
            state.is_final = not state.is_final