from scripts.automata import *

if __name__ == "__main__":
    automata = Automata.create_from_txt_file("data/ex6-6.txt")
    print(automata)
    print("Standard : ", automata.is_standard())
    automata.standardize()

    print(automata)
    print("Standard : ", automata.is_standard())
