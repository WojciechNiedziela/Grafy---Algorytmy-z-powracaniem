import argparse, copy, os, re

import Graph_time_class as Graph_time_class

Graph = Graph_time_class.Graph

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
            graph = Graph()
            actions = graph.load_graph_from_file(file_path)
            print(f"Loaded graph from {filename}:")

            while actions:
                action = actions.pop(0)
                if action.lower() == "exit":
                    break
                elif action.lower() == "euler":
                    graph.find_euler_cycle()
                else:
                    print(f"Nieznana komenda: {action}")

if __name__ == "__main__":
    main()
