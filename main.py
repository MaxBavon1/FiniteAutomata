from scripts.automata import *

if __name__ == "__main__":
    automata = Automata.create_from_txt_file("data/INT1-7-16.txt")
    automata.completion()
    print(f"Complete automata :{automata}")
    print(f"Is deterministic ? : {automata.is_deterministic()}")