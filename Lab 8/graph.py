from abc import ABC, abstractmethod
import polska


class Vertex:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)


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
    def delete_vertex(self, vertex):
        pass

    @abstractmethod
    def delete_edge(self, vertex1, vertex2):
        pass


class ListGraph(Graph):
    def __init__(self):
        self.neighbor_list = {}

    def is_empty(self):
        return len(self.neighbor_list) == 0

    def insert_vertex(self, vertex):
        self.neighbor_list[vertex] = {}

    def insert_edge(self, vertex1, vertex2, edge=None):
        if vertex1 in self.neighbor_list and vertex2 in self.neighbor_list:
            self.neighbor_list[vertex1][vertex2] = edge
            self.neighbor_list[vertex2][vertex1] = edge

    def delete_vertex(self, vertex):
        pass

    def delete_edge(self, vertex1, vertex2):
        pass

    def vertices(self):
        return self.neighbor_list.keys()

    def neighbours(self, vertex):
        return [(vert, self.neighbor_list[vertex][vert]) for vert in self.neighbor_list[vertex].keys()]


if __name__ == '__main__':
    graph = ListGraph()

    for n in polska.polska:
        graph.insert_vertex(Vertex(n[2]))

    for (ver1, vert2) in polska.graf:
        graph.insert_edge(Vertex(ver1), Vertex(vert2))

    polska.draw_map(graph)
