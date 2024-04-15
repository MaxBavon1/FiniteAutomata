from scripts.automata import *

if __name__ == "__main__":
    automata = Automata.create_from_txt_file("data/INT1-7-29.txt")

    print(automata)    
    automata.standardize()

    print(automata)
    #print("Standard : ", automata.is_standard())
    #test
