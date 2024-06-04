import random
import Node_class as Node_class

Node = Node_class.Node

class Graph:
    def __init__(self, nodes, saturation):
        self.nodes = [Node(i) for i in range(1, nodes + 1)]
        self.create_hamilton_graph(saturation)

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