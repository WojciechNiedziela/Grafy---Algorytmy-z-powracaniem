import random
import networkx as nx

def create_hamilton_graph(nodes, saturation):
    # Tworzenie cyklu Hamiltona
    cycle = list(range(nodes))
    random.shuffle(cycle)
    G = nx.Graph()
    G.add_nodes_from(cycle)
    G.add_edges_from([(cycle[i-1], cycle[i]) for i in range(nodes)])

    # Dodawanie dodatkowych krawędzi do grafu
    edges = nodes * (nodes - 1) // 2
    additional_edges = int(edges * saturation / 100) - nodes
    for _ in range(additional_edges):
        while True:
            u, v = random.sample(range(nodes), 2)
            if G.degree(u) % 2 == 0 and G.degree(v) % 2 == 0 and not G.has_edge(u, v):
                G.add_edge(u, v)
                break

    return G


G = create_hamilton_graph(4, 70)
print(G.edges)
