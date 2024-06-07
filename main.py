import argparse
import copy
import sys
import Graph_class as Graph_class

Graph = Graph_class.Graph

sys.setrecursionlimit(1000000000)

def help():
    print("Dostępne komendy:")
    print("  print      -       wydrukuj graf")
    print("  help       -       wyświetl dostępne komendy")
    print("  euler      -       znajdź cykl Eulera")
    print("  hamilton   -       znajdź cykl Hamiltona")
    print("  export     -       wyeksportuj graf do TikZ")
    print("  exit       -       zakończ program")

def get_valid_int(prompt, validation_fn=None, error_message="Nieprawidłowa wartość."):
    while True:
        try:
            value = int(input(prompt))
            if validation_fn and not validation_fn(value):
                print(error_message)
                continue
            return value
        except ValueError:
            print(error_message)

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument("--hamilton", action='store_true')
    parser.add_argument("--non-hamilton", action='store_true')
    args = parser.parse_args()

    if args.hamilton or args.non_hamilton:
        nodes = get_valid_int("nodes> ", lambda x: x % 2 == 0, "Liczba wierzchołków musi być parzysta, aby każdy wierzchołek był parzystego stopnia. Proszę wprowadzić parzystą liczbę.")
        
        if args.hamilton:
            saturation = get_valid_int("saturation> ", lambda x: x in [30, 70], "Nieprawidłowe nasycenie. Proszę wprowadzić 30 lub 70.")
            graph = Graph(nodes, saturation)
        
        elif args.non_hamilton:
            graph = Graph(nodes, 50, is_hamiltonian=False)

        while True:
            action = input("action> ").strip().lower()
            if action == "print":
                graph.print_graph()
            elif action == "help":
                help()
            elif action == "exit":
                break
            elif action == "euler":
                graph_tmp = copy.deepcopy(graph)
                euler_cycle = graph_tmp.find_euler_cycle()
                if euler_cycle:
                    print(" -> ".join(map(str, euler_cycle)))
                else:
                    print("Graf nie posiada cyklu Eulera.")
            elif action == "hamilton":
                hamilton_cycle = graph.find_hamiltonian_cycle()
                if hamilton_cycle:
                    print(" -> ".join(map(str, hamilton_cycle)))
                else:
                    print("Graf nie posiada cyklu Hamiltona.")
            elif action == "export":
                tikz = graph.export_to_tikz()
                with open("graph.tex", "w") as f:
                    f.write(tikz)
                print("Graf wyeksportowany do graph.tex.")
            else:
                print("Nieznana komenda. Dostępne komendy to: print, help, exit, euler, hamilton, export.")

if __name__ == "__main__":
    main()
