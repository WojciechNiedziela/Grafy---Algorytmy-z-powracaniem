class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

    def __repr__(self): 
        return f"Node({self.val})"
