##this is not the final version this is a version I found online 
##that I am using to help me build my own version of MaptoGraph.py
import networkx as nx

from collections import defaultdict

class CityGraph:
    def __init__(self):
        # Using adjacency list representation
        self.graph = defaultdict(list)

    def add_road(self, from_place, to_place, distance):
        """
        Adds a bidirectional road between two places.
        :param from_place: str - starting location
        :param to_place: str - ending location
        :param distance: float/int - distance or travel time
        """
        if distance <= 0:
            raise ValueError("Distance must be positive.")
        self.graph[from_place].append((to_place, distance))
        self.graph[to_place].append((from_place, distance))

    def get_graph(self):
        """Returns the adjacency list representation."""
        return dict(self.graph)

    def display(self):
        """Prints the graph in a readable format."""
        for place, roads in self.graph.items():
            connections = ", ".join([f"{dest} ({dist})" for dest, dist in roads])
            print(f"{place} -> {connections}")


# Example usage
if __name__ == "__main__":
    # Example city map: list of (from, to, distance)
    city_map_data = [
        ("A", "B", 5),
        ("A", "C", 10),
        ("B", "C", 3),
        ("B", "D", 7),
        ("C", "D", 2),
        ("D", "E", 4)
    ]

    city_graph = CityGraph()

    try:
        for road in city_map_data:
            city_graph.add_road(*road)

        print("City Graph Representation:")
        city_graph.display()

        # Access adjacency list
        print("\nAdjacency List:", city_graph.get_graph())

    except ValueError as e:
        print("Error:", e)