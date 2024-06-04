import os

base_directory = os.path.join('Time measuring', 'data')
os.makedirs(base_directory, exist_ok=True)

###########################################################################
n_start = 50
n_end = 1000
n_step = 50
saturation = 30
operation = "euler"
###########################################################################
n_values = range(n_start, n_end + 1, n_step)

for n in n_values:
    file_path = os.path.join(base_directory, f'graph_{n}.txt')
    with open(file_path, 'w') as f:
        f.write(f"{n}\n")
        f.write(f"{saturation}\n")
        if operation:
            f.write(f"{operation}\n")
        f.write("exit\n")

created_files = os.listdir(base_directory)
print("Created files:", created_files)
