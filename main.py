# Wybrana reprezentacja: lista sąsiedztwa - najbardziej efektywna, graf spójny, nieskierowany
# TODO:
#
# - clean code
# nie usuwac przy eulerze krawedzi z grafu

import argparse, random

class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

    def __repr__(self):  # Definicja metody __repr__ dla klasy Node
        return f"Node({self.val})"

def create_hamilton_graph(nodes, saturation):
    cycle = [Node(i) for i in range(1, nodes + 1)]
    random.shuffle(cycle)
    
    # Tworzenie cyklu Hamiltona
    for i in range(nodes):
        cycle[i-1].neighbors.append(cycle[i % nodes])
        cycle[i % nodes].neighbors.append(cycle[i-1])

    # Dodawanie dodatkowych krawędzi do grafu
    edges = nodes * (nodes - 1) // 2
    additional_edges = int(edges * saturation / 100) - nodes
    if additional_edges % 2 != 0:
        additional_edges += 1  # Upewniamy się, że liczba dodatkowych krawędzi jest parzysta
    additional_edges_needed = additional_edges

    while additional_edges_needed > 0:
        a, b, c = random.sample(cycle, 3)
        # Sprawdzamy, czy nie istnieją krawędzie między a, b i c
        if b not in a.neighbors and c not in a.neighbors and a not in b.neighbors and c not in b.neighbors and a not in c.neighbors and b not in c.neighbors:
            # Dodajemy krawędzie a-b, b-c i c-a
            a.neighbors.append(b)
            b.neighbors.append(a)
            b.neighbors.append(c)
            c.neighbors.append(b)
            c.neighbors.append(a)
            a.neighbors.append(c)
            additional_edges_needed -= 3  # Zmniejszamy liczbę potrzebnych krawędzi o 3

    return cycle

def print_graph(graph):
    for node in sorted(graph, key=lambda node: node.val):
        print(f"Wierzchołek {node.val}: {[neighbor.val for neighbor in node.neighbors]}")

def help():
    print("Dostępne komendy:")
    print("  print - wydrukuj graf")
    print("  help - wyświetl dostępne komendy")
    print("  exit - zakończ program")

def remove_edge(graph, v, u):
    for node in graph:
        if node.val == v.val and u in node.neighbors:
            node.neighbors.remove(u)
        if node.val == u.val and v in node.neighbors:
            node.neighbors.remove(v)

def DFS_Euler(v, graph, cycle, visited_edges):
    for u in v.neighbors[:]:  # Kopia listy sąsiedztwa, aby uniknąć modyfikacji podczas iteracji
        if (v, u) not in visited_edges:
            visited_edges.add((v, u))  # Oznaczam krawędź jako odwiedzoną
            visited_edges.add((u, v))  # Dodaję krawędź w obu kierunkach, ponieważ graf jest nieskierowany
            remove_edge(graph, v, u) 
            DFS_Euler(u, graph, cycle, visited_edges)
    cycle.append(v.val)  # v na stos

def find_euler_cycle(graph):
    cycle = []
    visited_edges = set()
    DFS_Euler(graph[0], graph, cycle, visited_edges)  # Rozpocznij DFS od pierwszego wierzchołka
    return cycle[::-1]  # Odwróć cykl, aby zacząć od początkowego wierzchołka

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument("--hamilton", action='store_true') 
    args = parser.parse_args()

    if args.hamilton:
        while True:
            nodes = int(input("nodes> "))
            if nodes % 2 == 0:
                break
            else:
                print("Liczba wierzchołków musi być parzysta, aby każdy wierzchołek był parzystego stopnia. Proszę wprowadzić parzystą liczbę.")
        while True:
            saturation = int(input("saturation> "))
            if saturation in [30, 70]:
                break
            else:
                print("Nieprawidłowe nasycenie. Proszę wprowadzić 30 lub 70.")
        Graph = create_hamilton_graph(nodes, saturation)

        while True:
            print("> ", end="")
            action = input().strip()
            if action.lower() == "print":
                print_graph(Graph)
            elif action.lower() == "help":
                help()
            elif action.lower() == "exit":
                break
            elif action.lower() == "euler":
                Graph_tmp = Graph.copy()
                euler_cycle = find_euler_cycle(Graph_tmp)
                if euler_cycle:
                        print(" -> ".join(map(str, euler_cycle)))
                else:
                    print("Graf nie posiada cyklu Eulera.")
            else:
                print("Nieznana komenda. Dostępne komendy to: print, help, exit.")

if __name__ == "__main__":
    main()
