# Wybrana reprezentacja: lista sąsiedztwa - najbardziej efektywna, graf spójny, nieskierowany

import argparse, random, copy

class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

    def __repr__(self): 
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

def remove_edge(graph, vNode, uNode):
    for node in graph:
        if node.val == vNode.val and uNode in node.neighbors:
            node.neighbors.remove(uNode)
        if node.val == uNode.val and vNode in node.neighbors:
            node.neighbors.remove(vNode)

def DFS_Euler(vNode, graph, eulerCycleResult, visited_edges):
    for uNode in vNode.neighbors[:]:
        if (vNode, uNode) not in visited_edges:
            visited_edges.add((vNode, uNode))  
            visited_edges.add((uNode, vNode)) 
            remove_edge(graph, vNode, uNode) 
            DFS_Euler(uNode, graph, eulerCycleResult, visited_edges)
    eulerCycleResult.append(vNode.val) 

def find_euler_cycle(graph):
    eulerCycleResult = []
    visited_edges = set()
    DFS_Euler(graph[0], graph, eulerCycleResult, visited_edges) 
    eulerCycleResult.reverse()  
    return eulerCycleResult

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
                Graph_tmp = copy.deepcopy(Graph)
                euler_cycle = find_euler_cycle(Graph_tmp)
                if euler_cycle:
                        print(" -> ".join(map(str, euler_cycle)))
                else:
                    print("Graf nie posiada cyklu Eulera.")
            else:
                print("Nieznana komenda. Dostępne komendy to: print, help, exit.")

if __name__ == "__main__":
    main()
