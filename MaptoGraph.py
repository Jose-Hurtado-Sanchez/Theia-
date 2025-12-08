import csv
import math
from pathlib import Path
from typing import Dict, Tuple, List

import networkx as nx


def parse_nodes(nodes_csv_path: Path) -> Dict[str, Dict]:
    
    #parse nodes from a CSV file.
    nodes: Dict[str, Dict] = {}

    with nodes_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            node_id = row["id"].strip()
            label = row.get("label", node_id).strip()
            x = float(row["x"])
            y = float(row["y"])
            nodes[node_id] = {"label": label, "pos": (x, y)}

    return nodes


def parse_edges(edges_csv_path: Path) -> List[Tuple[str, str]]:
    #parse edges from a CSV file.
    edges: List[Tuple[str, str]] = []

    with edges_csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["source"].strip()
            tgt = row["target"].strip()
            edges.append((src, tgt))

    return edges



def build_graph_from_floorplan(nodes: Dict[str, Dict],
                               edges: List[Tuple[str, str]]) -> nx.Graph:
    #buuild graph
    G = nx.Graph()

    # Add nodes
    for node_id, data in nodes.items():
        G.add_node(node_id, label=data["label"], pos=data["pos"])

    
    def compute_distance(u: str, v: str) -> float:
        x1, y1 = G.nodes[u]["pos"]
        x2, y2 = G.nodes[v]["pos"]
        return math.hypot(x2 - x1, y2 - y1)

    for u, v in edges:
        if u not in G.nodes:
            raise ValueError(f"unknown node id: {u}")
        if v not in G.nodes:
            raise ValueError(f"unknown node id: {v}")

        dist = compute_distance(u, v)
        G.add_edge(u, v, weight=dist)

    return G



def find_route(graph: nx.Graph, start_id: str, dest_id: str):
    
    
    path = nx.dijkstra_path(graph, source=start_id, target=dest_id, weight="weight")
    distance = nx.dijkstra_path_length(graph, source=start_id, target=dest_id, weight="weight")
    return path, distance


def path_to_text_directions(graph: nx.Graph, path: List[str]) -> List[str]:
    directions: List[str] = []

    for i in range(len(path) - 1):
        node_id = path[i]
        next_id = path[i + 1]

        node = graph.nodes[node_id]
        nxt = graph.nodes[next_id]

        segment = graph.edges[node_id, next_id]
        dist = segment["weight"]

        directions.append(
            f"From {node['label']}, walk approximately {dist:.1f} meters towards {nxt['label']}."
        )

    return directions




if __name__ == "__main__":
  
    nodes_csv = Path("nodes.csv")
    edges_csv = Path("edges.csv")

   
    nodes = parse_nodes(nodes_csv)
    edges = parse_edges(edges_csv)

    G = build_graph_from_floorplan(nodes, edges)

    start = "entrance"
    destination = "room_201"

    path, total_distance = find_route(G, start, destination)

    print("path:")
    print(" -> ".join(path))
    print(f"\nTotal distance: {total_distance:.1f} meters\n")

    
    for line in path_to_text_directions(G, path):
        print(" -", line)
