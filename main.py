from scripts.automata import *

if __name__ == "__main__":
    automata = Automata.create_from_txt_file("data/INT1-7-6.txt")

    print(automata)
    print(automata.is_complete())
    automata.completion()

    print(automata.is_complete())
    print(automata)

    print(f"Is deterministic ? : {automata.is_deterministic()}")
    automata.determinize()

    print(f"Is deterministic ? : {automata.is_deterministic()}")
    print(automata)

    automata.minimize()
    # print(f"Is deterministic ? : {automata.is_deterministic()}")