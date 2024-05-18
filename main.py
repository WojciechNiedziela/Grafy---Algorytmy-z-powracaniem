# Wybrana reprezentacja: lista sąsiedztwa
# TODO:
#
#
#

import argparse
import random

class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

def create_hamilton_graph(nodes, saturation):
    # Tworzenie cyklu Hamiltona
    cycle = [Node(i) for i in range(nodes)]
    random.shuffle(cycle)
    for i in range(nodes):
        cycle[i-1].neighbors.append(cycle[i])
        cycle[i].neighbors.append(cycle[i-1])

    # Build a list of all possible edges that could be added
    possible_edges = [(u, v) for u in range(nodes) for v in range(u+1, nodes)]
    random.shuffle(possible_edges)

    # Dodawanie dodatkowych krawędzi do grafu
    edges = nodes * (nodes - 1) // 2
    additional_edges = int(edges * saturation / 100) - nodes
    for u, v in possible_edges:
        if len(cycle[u].neighbors) % 2 == 0 and len(cycle[v].neighbors) % 2 == 0:
            cycle[u].neighbors.append(cycle[v])
            cycle[v].neighbors.append(cycle[u])
            additional_edges -= 1
            if additional_edges == 0:
                break

    return cycle

def print_graph(graph):
    for node in graph:
        print(f"Wierzchołek {node.val}: {[neighbor.val for neighbor in node.neighbors]}")

def help():
    print("Dostępne komendy:")
    print("  print - wydrukuj graf")
    print("  help - wyświetl dostępne komendy")
    print("  exit - zakończ program")

def find_euler_cycle(graph):
    # Sprawdź, czy wszystkie wierzchołki mają parzysty stopień
    for node in graph:
        if len(node.neighbors) % 2 != 0:
            return None  # Graf nie ma cyklu Eulera

    # Stos do przechowywania aktualnej ścieżki
    stack = [graph[0]]
    # Lista do przechowywania cyklu Eulera
    cycle = []

    while stack:
        current_node = stack[-1]
        # Jeśli bieżący wierzchołek ma sąsiadów, przenieś go na stos
        if current_node.neighbors:
            stack.append(current_node.neighbors.pop())
        # Jeśli bieżący wierzchołek nie ma sąsiadów, dodaj go do cyklu Eulera
        else:
            cycle.append(stack.pop())

    return cycle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hamilton", action='store_true')
    args = parser.parse_args()

    if args.hamilton:
        nodes = int(input("nodes> "))
        while True:
            saturation = int(input("saturation> "))
            if saturation in [30, 70]:
                break
            else:
                print("Nieprawidłowe nasycenie. Proszę wprowadzić 30 lub 70.")
        G = create_hamilton_graph(nodes, saturation)

        while True:
            print("> ", end="")
            action = input().strip()
            if action.lower() == "print":
                print_graph(G)
            elif action.lower() == "help":
                help()
            elif action.lower() == "exit":
                break
            elif action.lower() == "euler":
                find_euler_cycle(G)
            else:
                print("Nieznana komenda. Dostępne komendy to: print, help, exit.")

if __name__ == "__main__":
    main()
