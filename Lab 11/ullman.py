from abc import ABC, abstractmethod
import numpy as np
import copy


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
    def insert_edge(self, vertex1, vertex2):
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
        self.matrix = np.zeros((0, 0), dtype=int)

    def is_empty(self):
        return len(self.vertex) == 0

    def insert_vertex(self, vertex):
        h = hash(vertex)
        if h in self.vertex:
            raise Exception(f"Vertex {vertex} already exists")
        index = self.matrix.shape[0]
        self.vertex[h] = vertex
        self.indices[h] = index

        # Expand matrix
        if index == 0:
            self.matrix = np.zeros((1, 1), dtype=int)
        else:
            self.matrix = np.pad(self.matrix, ((0, 1), (0, 1)), mode='constant')

    def insert_edge(self, vertex1, vertex2):
        h1, h2 = hash(vertex1), hash(vertex2)
        if h1 not in self.indices or h2 not in self.indices:
            raise Exception("Vertexes do not exist")
        i1, i2 = self.indices[h1], self.indices[h2]
        self.matrix[i1][i2] = 1
        self.matrix[i2][i1] = 1

    def delete_vertex(self, vertex_id):
        if vertex_id not in self.vertex:
            raise Exception(f"Vertex {vertex_id} does not exist")
        index = self.indices[vertex_id]

        self.matrix = np.delete(self.matrix, index, axis=0)
        self.matrix = np.delete(self.matrix, index, axis=1)

        del self.vertex[vertex_id]
        del self.indices[vertex_id]

        for h, i in list(self.indices.items()):
            if i > index:
                self.indices[h] = i - 1

    def delete_edge(self, vertex1_id, vertex2_id):
        if vertex1_id not in self.indices or vertex2_id not in self.indices:
            raise Exception(f"Edge {vertex1_id}->{vertex2_id} does not exist")
        i1, i2 = self.indices[vertex1_id], self.indices[vertex2_id]
        self.matrix[i1][i2] = 0
        self.matrix[i2][i1] = 0

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
            if self.matrix[index][i] != 0:
                result.append((h, self.matrix[index][i]))
        return result

    def get_matrix(self):
        return self.matrix


# ullman(używane, aktualny_wiersz, macierz_M):
#     jeżeli aktualny_wiersz == liczba_wierszy:
#          wypisz M
#          return
#     dla każdej kolumny c:
#          jeżeli kolumna c jest  nieużywana (czyli False w liście używanych):
#               oznacz kolumnę c jako używaną
#               wypełnij aktualny_wiersz macierzy_M zerami i wstaw 1 do c-tego elementu wiersza
#               wywołaj rekurencyjnie ullman dla następnego wiersza
#               oznacz kolumnę c jako nieużywaną
def ullman(used, current, M, P, G, liczba_wywolan=0, liczba_izomorfizmow=0):
    liczba_wywolan += 1
    if current == M.shape[0]:
        if np.array_equal(P, M @ ((M @ G).transpose())):
            liczba_izomorfizmow += 1
        return liczba_wywolan, liczba_izomorfizmow
    for c in range(M.shape[1]):
        if c not in used:
            used.add(c)
            for r in range(M.shape[1]):
                M[current, r] = 0
            M[current, c] = 1
            liczba_wywolan, liczba_izomorfizmow = ullman(used, current + 1, M, P, G, liczba_wywolan,
                                                         liczba_izomorfizmow)
            used.remove(c)
    return liczba_wywolan, liczba_izomorfizmow


def ullman2(used, current, M, P, G, liczba_wywolan=0, liczba_izomorfizmow=0):
    liczba_wywolan += 1
    if current == M.shape[0]:
        if np.array_equal(P, M @ ((M @ G).transpose())):
            liczba_izomorfizmow += 1
        return liczba_wywolan, liczba_izomorfizmow

    for c in range(M.shape[1]):
        if c not in used and M[current, c] == 1:
            used.add(c)
            Mc = copy.deepcopy(M)
            Mc[current, :] = 0
            Mc[current, c] = 1
            liczba_wywolan, liczba_izomorfizmow = ullman2(
                used, current + 1, Mc, P, G, liczba_wywolan, liczba_izomorfizmow)
            used.remove(c)

    return liczba_wywolan, liczba_izomorfizmow


def ullman3(used, current, M, P, G, liczba_wywolan=0, liczba_izomorfizmow=0):
    liczba_wywolan += 1

    if current == M.shape[0]:
        if np.array_equal(P, M @ ((M @ G).transpose())):
            liczba_izomorfizmow += 1
        return liczba_wywolan, liczba_izomorfizmow

    for col in range(M.shape[1]):
        if col not in used and M[current][col] != 0:
            used.add(col)
            M_copy = copy.deepcopy(M)
            M_copy[current, :] = 0
            M_copy[current, col] = 1

            M_prune = prune(copy.deepcopy(M_copy), P, G)

            liczba_wywolan, liczba_izomorfizmow = ullman3(used, current + 1, M_prune, P, G, liczba_wywolan,
                                                          liczba_izomorfizmow)
            used.remove(col)
    return liczba_wywolan, liczba_izomorfizmow


def createM0(P, G):
    M0 = np.zeros((P.shape[0], G.shape[0]), dtype=int)
    sumP = np.sum(P, axis=1)
    sumG = np.sum(G, axis=1)

    for i in range(P.shape[0]):
        for j in range(G.shape[0]):
            if sumP[i] <= sumG[j]:
                M0[i][j] = 1
    return M0


def prune(M, P, G):
    changed = True
    while changed:
        changed = False
        rows, cols = M.shape
        for i in range(rows):
            for j in range(cols):
                if M[i][j] == 1:
                    p_neighs = [idx for idx, val in enumerate(P[i]) if val == 1]
                    g_neighs = [idx for idx, val in enumerate(G[j]) if val == 1]
                    for x in p_neighs:
                        if not any(M[x][y] == 1 for y in g_neighs):
                            M[i][j] = 0
                            changed = True
                            break
    return M


if __name__ == '__main__':
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    g1 = MatrixGraph()
    g2 = MatrixGraph()

    for c in ['A', 'B', 'C', 'D', 'E', 'F']:
        g1.insert_vertex(Vertex(c))

    for c in ['A', 'B', 'C']:
        g2.insert_vertex(Vertex(c))

    for s, t, v in graph_G:
        g1.insert_edge(Vertex(s), Vertex(t))

    for s, t, v in graph_P:
        g2.insert_edge(Vertex(s), Vertex(t))

    wynik1 = ullman(set(), 0, np.zeros((3, 6)), g2.get_matrix(), g1.get_matrix())
    M0 = createM0(g2.get_matrix(), g1.get_matrix())
    wynik2 = ullman2(set(), 0, M0, g2.get_matrix(), g1.get_matrix())
    M0 = createM0(g2.get_matrix(), g1.get_matrix())
    wynik3 = ullman3(set(), 0, M0, g2.get_matrix(), g1.get_matrix())
    print(wynik1[0], wynik1[1])
    print(wynik2[0], wynik2[1])
    print(wynik3[0], wynik3[1])
