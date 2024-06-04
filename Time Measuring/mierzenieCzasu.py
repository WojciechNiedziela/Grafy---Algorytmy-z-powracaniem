import argparse, random, copy, os, re, time, sys

sys.setrecursionlimit(1000000000)

class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

    def __repr__(self): 
        return f"Node({self.val})"

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        total_time = time.time() - start_time
        with open('results.txt', 'a') as f:  
            f.write(f"{total_time:.6f}\n")
        return result
    return wrapper

def create_hamilton_graph(nodes, saturation):
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
        if NodeB not in NodeA.neighbors and NodeC not in NodeA.neighbors and NodeA not in NodeB.neighbors and NodeC not in NodeB.neighbors and NodeA not in NodeC.neighbors and NodeB not in NodeC.neighbors:
            NodeA.neighbors.append(NodeB)
            NodeB.neighbors.append(NodeA)
            NodeB.neighbors.append(NodeC)
            NodeC.neighbors.append(NodeB)
            NodeC.neighbors.append(NodeA)
            NodeA.neighbors.append(NodeC)
            additional_edges_needed -= 3

    return cycle

def remove_edge(graph, vNode, uNode):
    for node in graph:
        if node.val == vNode.val and uNode in node.neighbors:
            node.neighbors.remove(uNode)
        if node.val == uNode.val and vNode in node.neighbors:
            node.neighbors.remove(vNode)

def DFS_Euler_iterative(start_node, graph):
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
            remove_edge(graph, vNode, unvisited)
            stack.append(unvisited)

    eulerCycleResult.reverse()
    return eulerCycleResult

@timer_decorator
def find_euler_cycle(graph):
    return DFS_Euler_iterative(graph[0], graph)

def load_graph_from_file(file_path):
    with open(file_path, 'r') as f:
        nodes = int(f.readline().strip())
        saturation = int(f.readline().strip())
        actions = []
        for line in f:
            actions.append(line.strip())
    
    graph = create_hamilton_graph(nodes, saturation)
    return graph, actions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hamilton_time", action='store_true')
    args = parser.parse_args()

    if args.hamilton_time:
        data_folder = 'data'
        files = os.listdir(data_folder)
        files = sorted(files, key=lambda f: int(re.search(r'graph_(\d+)', f).group(1)))

        for filename in files:
            file_path = os.path.join(data_folder, filename)
            graph, actions = load_graph_from_file(file_path)
            print(f"Loaded graph from {filename}:")

            while actions:
                action = actions.pop(0)
                if action.lower() == "exit":
                    break
                elif action.lower() == "euler":
                    graph_tmp = copy.deepcopy(graph)
                    find_euler_cycle(graph_tmp)
                else:
                    print(f"Nieznana komenda: {action}")

if __name__ == "__main__":
    main()
