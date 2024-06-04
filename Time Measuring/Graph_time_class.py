import random, time

import Node_time_class as Node_time_class

Node = Node_time_class.Node

class Graph:
    def __init__(self):
        self.graph = []

    def timer_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            total_time = time.time() - start_time
            with open('results.txt', 'a') as f:  
                f.write(f"{total_time:.6f}\n")
            return result
        return wrapper

    def create_hamilton_graph(self, nodes, saturation):
        cycle = [Node(i) for i in range(1, nodes + 1)]
        random.shuffle(cycle)

        for i in range(nodes):
            cycle[i-1].neighbors.append(cycle[i % nodes])
            cycle[i % nodes].neighbors.append(cycle[i-1])

        edges = nodes * (nodes - 1) // 2
        additional_edges = int(edges * saturation / 100) - nodes
        additional_edges_needed = additional_edges

        while additional_edges_needed > 0:
            NodeA, NodeB, NodeC = random.sample(cycle, 3)
            if (NodeB not in NodeA.neighbors and NodeC not in NodeA.neighbors and 
                NodeA not in NodeB.neighbors and NodeC not in NodeB.neighbors and 
                NodeA not in NodeC.neighbors and NodeB not in NodeC.neighbors):
                NodeA.neighbors.append(NodeB)
                NodeB.neighbors.append(NodeA)
                NodeB.neighbors.append(NodeC)
                NodeC.neighbors.append(NodeB)
                NodeC.neighbors.append(NodeA)
                NodeA.neighbors.append(NodeC)
                additional_edges_needed -= 3

        self.graph = cycle

    def remove_edge(self, vNode, uNode):
        for node in self.graph:
            if node.val == vNode.val and uNode in node.neighbors:
                node.neighbors.remove(uNode)
            if node.val == uNode.val and vNode in node.neighbors:
                node.neighbors.remove(vNode)

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

    @timer_decorator
    def find_euler_cycle(self):
        return self.DFS_Euler_iterative(self.graph[0])

    def load_graph_from_file(self, file_path):
        with open(file_path, 'r') as f:
            nodes = int(f.readline().strip())
            saturation = int(f.readline().strip())
            actions = []
            for line in f:
                actions.append(line.strip())

        self.create_hamilton_graph(nodes, saturation)
        return actions
