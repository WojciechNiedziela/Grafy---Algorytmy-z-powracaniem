import random
import math
import Node_class as Node_class

Node = Node_class.Node

class Graph:
    def __init__(self, nodes, saturation=0, is_hamiltonian=True):
        self.nodes = [Node(i) for i in range(1, nodes + 1)]
        if is_hamiltonian:
            if saturation > 0:
                self.create_hamilton_graph(saturation)
        else:
            self.create_non_hamilton_graph()

    def create_hamilton_graph(self, saturation):
        cycle = self.nodes[:]
        random.shuffle(cycle)

        for i in range(len(cycle)):
            cycle[i-1].add_neighbor(cycle[i % len(cycle)])
            cycle[i % len(cycle)].add_neighbor(cycle[i-1])

        edges = len(cycle) * (len(cycle) - 1) // 2
        additional_edges = int(edges * saturation / 100) - len(cycle)
        additional_edges_needed = additional_edges

        while additional_edges_needed > 0:
            NodeA, NodeB, NodeC = random.sample(cycle, 3)
            if (NodeB not in NodeA.neighbors and NodeC not in NodeA.neighbors and 
                NodeA not in NodeB.neighbors and NodeC not in NodeB.neighbors and 
                NodeA not in NodeC.neighbors and NodeB not in NodeC.neighbors):
                NodeA.add_neighbor(NodeB)
                NodeB.add_neighbor(NodeA)
                NodeB.add_neighbor(NodeC)
                NodeC.add_neighbor(NodeB)
                NodeC.add_neighbor(NodeA)
                NodeA.add_neighbor(NodeC)
                additional_edges_needed -= 3

    def create_non_hamilton_graph(self):
        cycle = self.nodes[:]
        random.shuffle(cycle)

        for i in range(len(cycle)):
            cycle[i-1].add_neighbor(cycle[i % len(cycle)])
            cycle[i % len(cycle)].add_neighbor(cycle[i-1])

        edges = len(cycle) * (len(cycle) - 1) // 2
        additional_edges = int(edges * 50 / 100) - len(cycle)
        additional_edges_needed = additional_edges

        while additional_edges_needed > 0:
            NodeA, NodeB = random.sample(cycle, 2)
            if NodeB not in NodeA.neighbors:
                NodeA.add_neighbor(NodeB)
                NodeB.add_neighbor(NodeA)
                additional_edges_needed -= 1

        # Izoluj jeden wierzchołek
        isolated_node = random.choice(self.nodes)
        for neighbor in isolated_node.neighbors[:]:
            isolated_node.remove_neighbor(neighbor)
            neighbor.remove_neighbor(isolated_node)

    def print_graph(self):
        for node in sorted(self.nodes, key=lambda node: node.val):
            print(f"Wierzchołek {node.val}: {[neighbor.val for neighbor in node.neighbors]}")

    def remove_edge(self, vNode, uNode):
        vNode.remove_neighbor(uNode)
        uNode.remove_neighbor(vNode)

    def DFS_Euler_iterative(self, start_node):
        eulerCycleResult = []
        visited_edges = set()
        stack = [start_node]

        while stack:
            vNode = stack[-1]
            unvisited = None
            for uNode in vNode.neighbors:
                if (vNode, uNode) not in visited_edges:
                    unvisited = uNode
                    break

            if unvisited is None:
                eulerCycleResult.append(stack.pop().val)
            else:
                visited_edges.add((vNode, unvisited))
                visited_edges.add((unvisited, vNode))
                self.remove_edge(vNode, unvisited)
                stack.append(unvisited)

        eulerCycleResult.reverse()
        return eulerCycleResult

    def find_euler_cycle(self):
        return self.DFS_Euler_iterative(self.nodes[0])

    def find_hamiltonian_cycle(self):
        path = []

        def backtrack(current_node):
            if len(path) == len(self.nodes):
                return path[0] in current_node.neighbors
            for neighbor in current_node.neighbors:
                if neighbor not in path:
                    path.append(neighbor)
                    if backtrack(neighbor):
                        return True
                    path.pop()
            return False

        for node in self.nodes:
            path = [node]
            if backtrack(node):
                return [n.val for n in path]
        return None

    def export_to_tikz(self):
        tikz_code = "\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}\n"
        angle = 2 * math.pi / len(self.nodes)
        radius = 5  # radius of the polygon
        for i, node in enumerate(self.nodes):
            x = radius * math.cos(i * angle)
            y = radius * math.sin(i * angle)
            tikz_code += f"\\node ({node.val}) at ({x}, {y}) {{{node.val}}};\n"
        for node in self.nodes:
            for neighbor in node.neighbors:
                if node.val < neighbor.val:
                    tikz_code += f"\\draw ({node.val}) -- ({neighbor.val});\n"
        tikz_code += "\\end{tikzpicture}\n\\end{document}"
        return tikz_code