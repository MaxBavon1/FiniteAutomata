from scripts.automata import *
import os

def main(choice, automata):
        print("1. Load an automata from a file")
        print("2. Save the automata to a file")
        print("3. Check if the automata is complete")
        print("4. Complete the automata")
        print("5. Check if the automata is deterministic")
        print("6. Determinize the automata")
        print("7. Minimize the automata")
        print("8. Exit\n")

        print(f"Choose the number of the action : {choice[0]}\n")

        if choice[0] == 1:
            n=0
            while n < 1 or n > 44:
                print(f"Choose the number of the file (between 1 and 44) : {choice[1]}\n")
                n = choice[1]
                print("Invalid number\n" ) if n < 1 or n > 44 else None

            automata = Automata.create_from_txt_file(f"data/INT1-7-{n}.txt")
            print(automata)
        
        elif automata is None:
            print("You first need to create an automata from a file !\n")

        elif choice[0] == 2:
            name = input("Enter the name of your file : ")
            automata.save_to_txt_file(f"saves/{name}.txt")
            print("done !\n")

        elif choice[0] == 3:
            print(automata)
            print(f"\nIs the automata complete ? : {automata.is_complete()}\n")

        elif choice[0] == 4:
            automata.completion()
            print(automata)

        elif choice[0] == 5:
            print(automata)
            print(f"\nIs the automata deterministic ? : {automata.is_deterministic()}\n")

        elif choice[0] == 6:
            automata.determinize()
            print(automata)

        elif choice[0] == 7:
            automata.minimize()
            print(automata)

        else:
            print("Invalid choice\n")
        
        return automata

num_of_files = 44



import sys

# Sauvegarder la sortie standard originale
original_stdout = sys.stdout


achieved = [i for i in range(2, 45) if i not in [31, 32, 33, 34, 35, 42]]
for num_file in achieved:
    with open(f'tracepaths/INT1-7-{num_file}.txt', 'w') as f:
        sys.stdout = f
        automata = main([1, num_file], None)
        main([3], automata)
        automata = main([4], automata)
        main([5], automata)
        automata = main([6], automata)
        automata = main([7], automata)



    

# Restaurer la sortie standard originale
sys.stdout = original_stdout


    # num_file = 40
    # automata = main([1, num_file], None)
    # main([3], automata)
    # automata = main([4], automata)
    # main([5], automata)
    # automata = main([6], automata)
    # automata = main([7], automata)



    