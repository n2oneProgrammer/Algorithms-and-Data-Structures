from abc import ABC, abstractmethod
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


class UnionFind:
    def __init__(self, vertices):
        self.parent = {}
        self.size = {v: 1 for v in vertices}

    def find(self, vertex: Vertex):
        if vertex not in self.parent:
            return vertex
        self.parent[vertex] = self.find(self.parent[vertex])

        return self.parent[vertex]

    def union(self, vertex1, vertex2):
        root1 = self.find(vertex1)
        root2 = self.find(vertex2)
        if root1 == root2:
            return
        if self.size[hash(root1)] < self.size[hash(root2)]:
            root1, root2 = root2, root1
        self.parent[root2] = root1
        self.size[hash(root1)] += self.size[hash(root2)]


def kruskal_MST(graph: Graph) -> Graph:
    edges = []
    for v in graph.vertices():
        for u, weight in graph.neighbours(v):
            if v < u:
                edges.append((weight, graph.get_vertex(v), graph.get_vertex(u)))

    edges.sort(key=lambda x: x[0])

    uf = UnionFind(graph.vertices())
    mst = ListGraph()

    for vertex_id in graph.vertices():
        mst.insert_vertex(graph.get_vertex(vertex_id))

    for weight, v, u in edges:
        if uf.find(v) != uf.find(u):
            uf.union(v, u)
            mst.insert_edge(v, u, weight)

    return mst


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

    out = kruskal_MST(g)
    printGraph(out)
