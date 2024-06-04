class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

    def __repr__(self): 
        return f"Node({self.val})"

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def remove_neighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)