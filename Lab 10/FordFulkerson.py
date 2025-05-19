from abc import ABC, abstractmethod


class Vertex:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        return str(self.key)


class Graph(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def insert_vertex(self, vertex):
        pass

    @abstractmethod
    def insert_edge(self, vertex1, vertex2, edge):
        pass

    @abstractmethod
    def delete_vertex(self, vertex_id):
        pass

    @abstractmethod
    def delete_edge(self, vertex1_id, vertex2_id):
        pass

    @abstractmethod
    def vertices(self):
        pass

    @abstractmethod
    def get_vertex(self, vertex_id):
        pass

    @abstractmethod
    def neighbours(self, vertex_id):
        pass

    @abstractmethod
    def get_edge(self, vertex1_id, vertex2_id):
        pass


class ListGraph(Graph):
    def __init__(self):
        self.neighbor_list = {}
        self.vertex = {}

    def is_empty(self):
        return len(self.neighbor_list) == 0

    def insert_vertex(self, vertex):
        if hash(vertex) in self.vertex:
            raise Exception('Vertex {} already exists'.format(str(vertex)))
        self.neighbor_list[hash(vertex)] = {}
        self.vertex[hash(vertex)] = vertex

    def insert_edge(self, vertex1, vertex2, edge):
        if hash(vertex1) in self.neighbor_list and hash(vertex2) in self.neighbor_list:
            self.neighbor_list[hash(vertex1)][hash(vertex2)] = edge
        else:
            raise Exception("Vertexes do not exist")

    def delete_vertex(self, vertex_id):
        if vertex_id not in self.vertex:
            raise Exception("Vertex {} does not exist".format(str(vertex_id)))
        del self.vertex[vertex_id]
        del self.neighbor_list[vertex_id]
        for key in self.neighbor_list.keys():
            if vertex_id in self.neighbor_list[key]:
                del self.neighbor_list[key][vertex_id]

    def delete_edge(self, vertex1_id, vertex2_id):
        if vertex1_id not in self.neighbor_list or vertex2_id not in self.neighbor_list[vertex1_id]:
            raise Exception("Edge {}->{} do not exist".format(str(vertex1_id), str(vertex2_id)))
        del self.neighbor_list[vertex1_id][vertex2_id]
        del self.neighbor_list[vertex2_id][vertex1_id]

    def vertices(self):
        return self.vertex.keys()

    def get_vertex(self, vertex_id):
        if vertex_id not in self.vertex:
            raise Exception("Vertex {} does not exist".format(str(vertex_id)))
        return self.vertex[vertex_id]

    def neighbours(self, vertex_id):
        if vertex_id not in self.vertex:
            raise Exception("Vertex {} does not exist".format(str(vertex_id)))
        return self.neighbor_list[vertex_id].items()

    def get_edge(self, vertex1_id, vertex2_id):
        return self.neighbor_list[vertex1_id].get(vertex2_id, None)


def printGraph(g):
    print("------GRAPH------")
    for v in g.vertices():
        print(g.get_vertex(v), end=" -> ")
        for (n, w) in g.neighbours(v):
            print(g.get_vertex(n), w, end=";")
        print()
    print("-------------------")


class Edge:
    def __init__(self, capacity: float, is_residual: bool = False):
        self.capacity = capacity
        self.flow = 0
        self.residual_capacity = 0 if is_residual else capacity
        self.is_residual = is_residual

    def __repr__(self):
        return f"{self.capacity} {self.flow} {self.residual_capacity} {self.is_residual}"


def bfs(graph: Graph, source: int, target: int) -> dict[int, int]:
    visited: set[int] = set()
    parent: dict[int, int] = {}
    queue: list[int] = [source]
    visited.add(source)

    while len(queue) > 0:
        current = queue.pop(0)
        for neighbor, edge in graph.neighbours(current):
            if neighbor not in visited and edge.residual_capacity > 0:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current
                if neighbor == target:
                    return parent
    return parent


def find_path_capacity(graph: Graph, source: int, target: int, parent: dict[int, int]) -> int:
    if target not in parent:
        return 0

    min_capacity = float('inf')
    v = target
    while v != source:
        u = parent[v]
        edge = graph.get_edge(u, v)
        min_capacity = min(min_capacity, edge.residual_capacity)
        v = u
    return min_capacity


def augment_path(graph: Graph, source: int, target: int, parent: dict[int, int], flow: int):
    v = target
    while v != source:
        u = parent[v]

        edge1 = graph.get_edge(u, v)
        edge1.residual_capacity -= flow

        edge2 = graph.get_edge(v, u)
        edge2.residual_capacity += flow

        if edge1.is_residual:
            edge2.flow -= flow
        else:
            edge1.flow += flow

        v = u


def fold_fulkerson(edges: list[tuple[int, int, int]], source: int, target: int) -> (int, Graph):
    g = ListGraph()
    for u, v, cap in edges:
        v_u = Vertex(u)
        v_v = Vertex(v)
        if hash(v_u) not in g.vertices():
            g.insert_vertex(v_u)
        if hash(v_v) not in g.vertices():
            g.insert_vertex(v_v)
        g.insert_edge(v_u, v_v, Edge(cap, is_residual=False))
        g.insert_edge(v_v, v_u, Edge(0, is_residual=True))

    max_flow = 0
    while True:
        parent = bfs(g, source, target)
        flow = find_path_capacity(g, source, target, parent)
        if flow == 0:
            break
        augment_path(g, source, target, parent, flow)
        max_flow += flow

    return max_flow, g

def test_case(edges):
    maxflow, graf = fold_fulkerson(edges, hash(Vertex('s')), hash(Vertex('t')))
    print(maxflow)
    printGraph(graf)


if __name__ == "__main__":
    print("Graph1:")
    test_case([('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)])

    print("Graph2:")
    test_case(
        [('s', 'a', 16), ('s', 'c', 13), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9), ('b', 't', 20), ('c', 'd', 14),
         ('d', 'b', 7), ('d', 't', 4)])

    print("Graph3:")
    test_case(
        [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
         ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)])
