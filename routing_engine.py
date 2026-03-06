"""
routing_engine.py
--------------------------------------------------
Dynamic Pathfinding & Logistics Optimization Engine

✔ No static datasets
✔ No authentication logic
✔ No API logic
✔ Fully dynamic graph input
✔ Shortest path (Dijkstra)
✔ A* pathfinding
✔ Multi-stop logistics optimization
✔ Emission-aware cost modeling
"""

from typing import Dict, List, Tuple, Optional
import heapq
import math


class RoutingEngine:
    """
    Dynamic graph-based routing and logistics optimizer.
    """

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, graph: Dict[str, Dict[str, float]]):
        """
        Graph format:
        {
            "A": {"B": 10, "C": 15},
            "B": {"A": 10, "D": 12},
            ...
        }
        """
        self._validate_graph(graph)
        self.graph = graph

    # ==========================================================
    # DIJKSTRA SHORTEST PATH
    # ==========================================================

    def shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """
        Returns shortest path and total distance using Dijkstra.
        """
        if start not in self.graph or end not in self.graph:
            raise ValueError("Start or end node not in graph")

        queue = [(0, start, [])]
        visited = set()

        while queue:
            cost, node, path = heapq.heappop(queue)

            if node in visited:
                continue

            visited.add(node)
            path = path + [node]

            if node == end:
                return path, cost

            for neighbor, weight in self.graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))

        raise ValueError("No path found")

    # ==========================================================
    # A* PATHFINDING
    # ==========================================================

    def a_star(
        self,
        start: str,
        end: str,
        coordinates: Dict[str, Tuple[float, float]]
    ) -> Tuple[List[str], float]:
        """
        A* pathfinding using Euclidean heuristic.
        """

        def heuristic(a, b):
            x1, y1 = coordinates[a]
            x2, y2 = coordinates[b]
            return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        open_set = [(0, start)]
        came_from = {}
        g_score = {node: float("inf") for node in self.graph}
        g_score[start] = 0

        f_score = {node: float("inf") for node in self.graph}
        f_score[start] = heuristic(start, end)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end:
                return self._reconstruct_path(came_from, current), g_score[end]

            for neighbor, weight in self.graph[current].items():
                tentative_g = g_score[current] + weight

                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        raise ValueError("No path found")

    # ==========================================================
    # MULTI-STOP ROUTE OPTIMIZATION (Greedy TSP Approximation)
    # ==========================================================

    def optimize_multi_stop_route(
        self,
        start: str,
        stops: List[str]
    ) -> Tuple[List[str], float]:
        """
        Greedy nearest-neighbor logistics optimizer.
        """

        if start not in self.graph:
            raise ValueError("Start node not in graph")

        remaining = stops[:]
        route = [start]
        total_cost = 0
        current = start

        while remaining:
            nearest = None
            min_cost = float("inf")

            for stop in remaining:
                _, cost = self.shortest_path(current, stop)
                if cost < min_cost:
                    nearest = stop
                    min_cost = cost

            route.append(nearest)
            total_cost += min_cost
            current = nearest
            remaining.remove(nearest)

        return route, total_cost

    # ==========================================================
    # EMISSION-AWARE COST MODEL
    # ==========================================================

    def calculate_emission_cost(
        self,
        distance: float,
        emission_rate_per_km: float
    ) -> float:
        """
        Calculates emission impact for route.
        """
        return distance * emission_rate_per_km

    # ==========================================================
    # INTERNAL UTILITIES
    # ==========================================================

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path

    def _validate_graph(self, graph):
        if not isinstance(graph, dict):
            raise TypeError("Graph must be dictionary")

        for node, neighbors in graph.items():
            if not isinstance(neighbors, dict):
                raise TypeError("Neighbors must be dictionary")

            for neighbor, weight in neighbors.items():
                if not isinstance(weight, (int, float)):
                    raise TypeError("Edge weights must be numeric")
                if weight <= 0:
                    raise ValueError("Edge weights must be positive")


# ==========================================================
# TEST BLOCK
# ==========================================================

if __name__ == "__main__":

    # Dynamic graph (example only for testing)
    graph_data = {
        "A": {"B": 10, "C": 15},
        "B": {"A": 10, "D": 12, "E": 15},
        "C": {"A": 15, "F": 10},
        "D": {"B": 12, "E": 2},
        "E": {"B": 15, "D": 2, "F": 5},
        "F": {"C": 10, "E": 5}
    }

    coordinates = {
        "A": (0, 0),
        "B": (2, 3),
        "C": (5, 2),
        "D": (6, 6),
        "E": (8, 3),
        "F": (7, 1)
    }

    engine = RoutingEngine(graph_data)

    path, distance = engine.shortest_path("A", "F")
    print("Shortest Path:", path, "Distance:", distance)

    path_astar, dist_astar = engine.a_star("A", "F", coordinates)
    print("A* Path:", path_astar, "Distance:", dist_astar)

    route, total = engine.optimize_multi_stop_route("A", ["D", "F", "E"])
    print("Optimized Route:", route, "Total Distance:", total)

    emission = engine.calculate_emission_cost(distance, emission_rate_per_km=0.2)
    print("Emission Cost:", emission)