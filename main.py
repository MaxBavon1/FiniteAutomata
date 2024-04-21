from scripts.automata import *
import os

if __name__ == "__main__":
    automata = None
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        print("1. Load an automata from a file")
        print("2. Save the automata to a file")
        print("3. Check if the automata is complete")
        print("4. Complete the automata")
        print("5. Check if the automata is deterministic")
        print("6. Determinize the automata")
        print("7. Minimize the automata")
        print("8. Exit\n")

        choice = int(input("Enter your choice : "))
        os.system('cls' if os.name == 'nt' else 'clear')

        

        if choice == 1:
            n=0
            while n < 1 or n > 44:
                n = int(input("Enter the number of the file : "))
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Invalid number\n" ) if n < 1 or n > 44 else None

            automata = Automata.create_from_txt_file(f"data/INT1-7-{n}.txt")
            os.system('cls' if os.name == 'nt' else 'clear')
            print(automata)
        
        elif automata is None:
            print("You first need to create an automata from a file !\n")

        elif choice == 2:
            name = input("Enter the name of your file : ")
            automata.save_to_txt_file(f"saves/{name}.txt")
            os.system('cls' if os.name == 'nt' else 'clear')
            print("done !\n")

        elif choice == 3:
            print(automata)
            print(f"\nIs the automata complete ? : {automata.is_complete()}\n")

        elif choice == 4:
            automata.completion()
            print(automata)

        elif choice == 5:
            print(automata)
            print(f"\nIs the automata deterministic ? : {automata.is_deterministic()}\n")

        elif choice == 6:
            automata.determinize()
            print(automata)

        elif choice == 7:
            #automata.minimize()
            print("not done yet\n")

        elif choice == 8:
            break

        else:
            print("Invalid choice\n")