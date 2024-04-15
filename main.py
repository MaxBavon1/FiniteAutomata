from scripts.automata import *

if __name__ == "__main__":
    automata = Automata.create_from_txt_file("data/INT1-7-9.txt")
    print(automata)
    automata.completion()
    print(automata)
