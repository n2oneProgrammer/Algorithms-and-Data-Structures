from abc import ABC, abstractmethod
import polska


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


class MatrixGraph(Graph):
    def __init__(self):
        self.vertex = {}
        self.indices = {}
        self.matrix = []

    def is_empty(self):
        return len(self.vertex) == 0

    def insert_vertex(self, vertex):
        h = hash(vertex)
        if h in self.vertex:
            raise Exception(f"Vertex {vertex} already exists")
        index = len(self.matrix)
        self.vertex[h] = vertex
        self.indices[h] = index

        for row in self.matrix:
            row.append(None)
        self.matrix.append([None] * (index + 1))

    def insert_edge(self, vertex1, vertex2, edge=1):
        h1, h2 = hash(vertex1), hash(vertex2)
        if h1 not in self.indices or h2 not in self.indices:
            raise Exception("Vertexes do not exist")
        i1, i2 = self.indices[h1], self.indices[h2]
        self.matrix[i1][i2] = edge
        self.matrix[i2][i1] = edge

    def delete_vertex(self, vertex_id):
        if vertex_id not in self.vertex:
            raise Exception(f"Vertex {vertex_id} does not exist")
        index = self.indices[vertex_id]

        self.matrix.pop(index)
        for row in self.matrix:
            row.pop(index)

        del self.vertex[vertex_id]
        del self.indices[vertex_id]

        for h, i in list(self.indices.items()):
            if i > index:
                self.indices[h] = i - 1

    def delete_edge(self, vertex1_id, vertex2_id):
        if vertex1_id not in self.indices or vertex2_id not in self.indices:
            raise Exception(f"Edge {vertex1_id}->{vertex2_id} does not exist")
        i1, i2 = self.indices[vertex1_id], self.indices[vertex2_id]
        self.matrix[i1][i2] = None
        self.matrix[i2][i1] = None

    def vertices(self):
        return self.vertex.keys()

    def get_vertex(self, vertex_id):
        if vertex_id not in self.vertex:
            raise Exception(f"Vertex {vertex_id} does not exist")
        return self.vertex[vertex_id]

    def neighbours(self, vertex_id):
        if vertex_id not in self.indices:
            raise Exception(f"Vertex {vertex_id} does not exist")
        index = self.indices[vertex_id]
        result = []
        for h, i in self.indices.items():
            if self.matrix[index][i] is not None:
                result.append((h, self.matrix[index][i]))
        return result


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

    def insert_edge(self, vertex1, vertex2, edge=1):
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


if __name__ == '__main__':
    option = input("1-macierz sąsiedstwa, 2-lista sąsiedzstwa: ")
    if option == '1':
        graph = MatrixGraph()
    elif option == '2':
        graph = ListGraph()
    else:
        raise Exception("bledny argument")
    for n in polska.polska:
        graph.insert_vertex(Vertex(n[2]))

    for (ver1, vert2) in polska.graf:
        graph.insert_edge(Vertex(ver1), Vertex(vert2))

    graph.delete_vertex(hash(Vertex('K')))
    graph.delete_edge(hash(Vertex('W')), hash(Vertex('E')))

    polska.draw_map(graph)
