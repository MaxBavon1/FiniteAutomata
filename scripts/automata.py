from typing import List
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
            # --- Alphabet ---
            alphabet = data.readline()
            if not alphabet:
                print("Error: Empty file")
                return
            alphabet = alphabet.replace('\n', '').split(',')
            automata = Automata(alphabet, [])

            # --- States ---
            num_states = data.readline()
            states = [State(automata, i, False, False) for i in range(int(num_states))]

            initial_states = data.readline()
            if initial_states != '\n':
                initial_states = initial_states.split(',')

                for state in initial_states:
                    states[int(state)].is_initial = True


            final_states = data.readline()
            if final_states != '\n':
                final_states = final_states.split(',')

                for state in final_states:
                    states[int(state)].is_final = True

            # --- Transitions ---
            transitions = data.readline()
            if transitions:
                transitions = transitions.split(',')

                for transition in transitions:
                    initial, label, final = transition.split(' ')
                    states[int(initial)].add_transition(label, states[int(final)])

        automata.states = states
        return automata

    def save_to_txt_file(self, path: str):
        with open(path, 'w') as file:
            file.write(','.join(self.alphabet) + '\n')
            file.write(str(self.num_states) + '\n')
            file.write(','.join(str(state.state) for state in self.initial_states) + '\n')
            file.write(','.join(str(state.state) for state in self.final_states) + '\n')
            for transition in self.transitions:
                file.write(f"{transition[0].state},{transition[1]},{transition[2].state}")

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
    
    def determinize(self):
        if not self.is_deterministic():

            # Initialization
            initial_closure = frozenset(self.initial_states)
            state_map = {initial_closure: State(self, 0, True, any(s.is_final for s in initial_closure))}
            new_states = [state_map[initial_closure]]
            queue = [initial_closure]

            # Process each set of states
            while queue:
                current_set = queue.pop(0)
                label_to_states = {}

                # Collect transitions for all states in the current set
                for state in current_set:
                    for label, next_states in state.transitions.items():
                        if label not in label_to_states:
                            label_to_states[label] = set()
                        label_to_states[label].update(next_states)

                # For each label, determine the next set of states
                for label, next_states in label_to_states.items():
                    next_set = frozenset(next_states)
                    if next_set not in state_map:
                        is_final = any(state.is_final for state in next_states)
                        new_state_id = len(new_states)
                        new_state = State(self, new_state_id, False, is_final)
                        state_map[next_set] = new_state
                        new_states.append(new_state)
                        queue.append(next_set)

                    # Add transition from the current set to the new set of states
                    current_state = state_map[current_set]
                    next_state = state_map[next_set]
                    current_state.add_transition(label, next_state)

            # Update the automaton's states with the new DFA states
            self.states = new_states
    
    def complementary(self):
        for state in self.states:
            state.is_final = not state.is_final

    def minimize(self):
        # Step 1: Remove unreachable states
        reachable_states = set()
        queue = self.initial_states[:]
        while queue:
            state = queue.pop(0)
            if state in reachable_states:
                continue
            reachable_states.add(state)
            for label, states in state.transitions.items():
                queue.extend(states)

        self.states = [state for state in self.states if state in reachable_states]

        # Step 2: Merge equivalent states using partition refinement
        # Initial partition: final states and non-final states
        partition = [set(self.final_states), set(state for state in self.states if not state.is_final)]
        previous_partition = []

        # Refine partition until it stabilizes
        while partition != previous_partition:
            previous_partition = partition[:]
            partition = []
            for group in previous_partition:
                # Split each group by distinguishable states
                labeled_groups = {}
                for state in group:
                    label_signature = tuple(sorted((label, frozenset(next_states)) for label, next_states in state.transitions.items()))
                    if label_signature not in labeled_groups:
                        labeled_groups[label_signature] = []
                    labeled_groups[label_signature].append(state)
                partition.extend(labeled_groups.values())

        # Create new states for each group in the final partition
        new_states = []
        state_mapping = {}
        for group in partition:
            new_state = State(self, len(new_states), any(s.is_initial for s in group), any(s.is_final for s in group))
            new_states.append(new_state)
            for state in group:
                state_mapping[state] = new_state

        # Rebuild transitions for new states
        for state in new_states:
            original_states = [original for original in self.states if state_mapping.get(original) == state]
            for original in original_states:
                for label, targets in original.transitions.items():
                    # Only add a transition if targets is not empty and the target is in the state mapping
                    if targets and state_mapping.get(targets[0]):
                        state.add_transition(label, state_mapping[targets[0]])


        self.states = new_states
