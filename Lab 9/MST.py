from abc import ABC, abstractmethod
from typing import Dict, Set

from graf_mst import graf


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
    def insert_edge(self, vertex1, vertex2, edge=None):
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

    def insert_edge(self, vertex1, vertex2, edge: float = 1):
        if hash(vertex1) in self.neighbor_list and hash(vertex2) in self.neighbor_list:
            self.neighbor_list[hash(vertex1)][hash(vertex2)] = edge
            self.neighbor_list[hash(vertex2)][hash(vertex1)] = edge
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


def printGraph(g):
    print("------GRAPH------")
    for v in g.vertices():
        print(g.get_vertex(v), end=" -> ")
        for (n, w) in g.neighbours(v):
            print(g.get_vertex(n), w, end=";")
        print()
    print("-------------------")


def prim_MST(graf: Graph):
    intree: Set[int] = set()
    distance: Dict[int, float] = {}
    parent: Dict[int, int] = {}
    sum_all = 0
    result_MST = ListGraph()
    v = list(graf.vertices())[0]
    for vertex in graf.vertices():
        distance[vertex] = float('inf')
    distance[v] = 0
    result_MST.insert_vertex(graf.get_vertex(v))
    while v not in intree:
        intree.add(v)
        neighbours = graf.neighbours(v)
        for v2, d in neighbours:
            if d < distance[v2] and v2 not in intree:
                distance[v2] = d
                parent[v2] = v

        min_vert: int | None = None
        for vertex in graf.vertices():
            if vertex in intree:
                continue
            if min_vert is None or distance[vertex] < distance[min_vert]:
                min_vert = vertex
        result_MST.insert_vertex(graf.get_vertex(min_vert))
        result_MST.insert_edge(graf.get_vertex(parent[min_vert]), graf.get_vertex(min_vert), distance[min_vert])
        sum_all += distance[min_vert]
        v = min_vert
    return result_MST


if __name__ == '__main__':
    g = ListGraph()
    for edge in graf:
        try:
            g.insert_vertex(Vertex(edge[0]))
        except:
            pass
        try:
            g.insert_vertex(Vertex(edge[1]))
        except:
            pass

        g.insert_edge(Vertex(edge[0]), Vertex(edge[1]), edge[2])

    out = prim_MST(g)
    printGraph(out)
