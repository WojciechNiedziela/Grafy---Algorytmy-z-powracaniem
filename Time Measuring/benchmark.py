import os
import networkx as nx

# Define the directory and ensure it exists
data_directory = 'data'
os.makedirs(data_directory, exist_ok=True)

# Function to create a Hamiltonian cycle graph
def create_hamiltonian_cycle_graph(n):
    G = nx.cycle_graph(n)
    return G

# Define the range for n values and the step
n_start = 50
n_end = 1000
n_step = 50
saturation = 30
operation = "euler"

# Generate the range of n values
n_values = range(n_start, n_end + 1, n_step)

# Generate the graphs and save them to files
for n in n_values:
    G = create_hamiltonian_cycle_graph(n)
    file_path = os.path.join(data_directory, f'graph_{n}.txt')
    with open(file_path, 'w') as f:
        f.write(f"{n}\n")
        f.write(f"{saturation}\n")
        if operation:
            f.write(f"{operation}\n")
        f.write("exit\n")

# Listing the created files for confirmation
created_files = os.listdir(data_directory)
print("Created files:", created_files)
