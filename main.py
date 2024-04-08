from scripts.automata import *

if __name__ == "__main__":
    automata = Automata.create_from_txt_file("data/automatas.txt")
    print(automata)