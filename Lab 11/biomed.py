import math

import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(str(self.x) + "x" + str(self.y))

    def __repr__(self):
        return str(self.x) + "x" + str(self.y)


class Edge:
    def __init__(self, I, theta):
        self.I = I
        self.theta = theta


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
            return
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

    def plot_graph(self, v_color, e_color):
        for idx, v in enumerate(self.vertex):
            x = self.get_vertex(v).x
            y = self.get_vertex(v).y
            plt.scatter(x, y, c=v_color)
            for n_idx, _ in self.neighbours(v):
                xn = self.get_vertex(n_idx).x
                yn = self.get_vertex(n_idx).y
                plt.plot([x, xn], [y, yn], color=e_color)


def unclutter_biometric_graph(graph: ListGraph):
    to_remove = set()
    to_add = []

    for v_id in list(graph.vertices()):
        neighbours = list(graph.neighbours(v_id))
        if len(neighbours) != 2:
            # Punkt charakterystyczny - start śledzenia
            for n_id, _ in neighbours:
                path = []
                current = n_id
                prev = v_id

                while True:
                    if current in to_remove:
                        break

                    current_neigh = list(graph.neighbours(current))
                    if len(current_neigh) != 2:
                        # Napotkaliśmy punkt końcowy śledzenia
                        to_add.append((v_id, current))  # Dodaj nową krawędź
                        to_add.append((current, v_id))
                        break

                    path.append(current)
                    to_remove.add(current)

                    # Wybieramy kolejny wierzchołek, pomijając tego, z którego przyszliśmy
                    next_candidates = [nid for nid, _ in current_neigh if nid != prev]
                    if not next_candidates:
                        break  # pętla się kończy — nie znaleziono innej ścieżki
                    prev, current = current, next_candidates[0]

    # Usuwanie wierzchołków
    for v_id in to_remove:
        graph.delete_vertex(v_id)

    # Dodanie nowych krawędzi
    for v1_id, v2_id in to_add:
        try:
            v1 = graph.get_vertex(v1_id)
            v2 = graph.get_vertex(v2_id)
            graph.insert_edge(v1, v2, Edge(I=1, theta=0))  # Możesz zmodyfikować I i theta
        except Exception:
            pass  # Jeśli któryś z wierzchołków został już usunięty lub nie istnieje


def merge_near_vertices(graph: ListGraph, thr=3):
    visited = set()
    groups = []

    vertex_items = list(graph.vertex.items())

    # Tworzymy listy grup wierzchołków do połączenia
    for i in range(len(vertex_items)):
        v1_id, v1 = vertex_items[i]
        if v1_id in visited:
            continue
        group = [v1]
        visited.add(v1_id)

        for j in range(i + 1, len(vertex_items)):
            v2_id, v2 = vertex_items[j]
            if v2_id in visited:
                continue

            dist = math.hypot(v1.x - v2.x, v1.y - v2.y)
            if dist < thr:
                group.append(v2)
                visited.add(v2_id)

        if len(group) > 1:
            groups.append(group)

    # Teraz przetwarzamy każdą grupę
    for group in groups:
        all_neighbors = set()
        group_ids = set([hash(v) for v in group])

        # Oblicz średnią współrzędnych
        avg_x = int(sum(v.x for v in group) / len(group))
        avg_y = int(sum(v.y for v in group) / len(group))
        new_vertex = Vertex(avg_x, avg_y)
        graph.insert_vertex(new_vertex)

        # Zbieramy połączenia z wierzchołków w grupie
        for v in group:
            v_id = hash(v)
            for n_id, edge in graph.neighbours(v_id):
                if n_id not in group_ids:
                    all_neighbors.add((n_id, edge))

        # Usuwamy stare wierzchołki
        for v in group:
            try:
                graph.delete_vertex(hash(v))
            except:
                pass  # może być już usunięty przez wcześniejsze połączenie

        # Dodajemy nowe krawędzie do sąsiadów
        for n_id, edge in all_neighbors:
            try:
                neighbor = graph.get_vertex(n_id)
                graph.insert_edge(new_vertex, neighbor, edge)
                graph.insert_edge(neighbor, new_vertex, edge)
            except:
                pass  # jeżeli neighbor już nie istnieje


def fill_biometric_graph_from_image(obraz, graph):
    h, w = obraz.shape
    for y in range(h):
        for x in range(w):
            if obraz[y, x] > 0:
                graph.insert_vertex(Vertex(x, y))
                for pos in [(-1, -1), (-1, 0), (0, -1), (1, -1)]:
                    nx, ny = x + pos[0], y + pos[1]
                    if obraz[ny, nx] > 0:
                        graph.insert_vertex(Vertex(nx, ny))
                        graph.insert_edge(Vertex(nx, ny), Vertex(x, y), 1)
                        graph.insert_edge(Vertex(x, y), Vertex(nx, ny), 1)


def angle_between_vectors(v1, v2):
    dot = np.dot(v1, v2)
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return np.arccos(np.clip(dot / norm, -1.0, 1.0))


def edge_vector(graph, v1_id, v2_id):
    v1 = graph.get_vertex(v1_id)
    v2 = graph.get_vertex(v2_id)
    return np.array([v2.x - v1.x, v2.y - v1.y]), v1, v2


def transform_graph(graph, ref_v1, ref_v2):
    # Wektor krawędzi
    vec = np.array([ref_v2.x - ref_v1.x, ref_v2.y - ref_v1.y])
    vec_norm = vec / np.linalg.norm(vec)
    angle = np.arccos(np.clip(np.dot(vec_norm, [1, 0]), -1.0, 1.0))

    if vec_norm[1] < 0:
        angle = -angle

    cos_theta, sin_theta = np.cos(-angle), np.sin(-angle)
    R = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])
    t = np.array([ref_v1.x, ref_v1.y])

    new_graph = ListGraph()
    for v_id in graph.vertices():
        v = graph.get_vertex(v_id)
        p = np.array([v.x, v.y]) - t
        p_rot = R @ p
        new_graph.insert_vertex(Vertex(p_rot[0], p_rot[1]))

    for v_id in graph.vertices():
        v = graph.get_vertex(v_id)
        for n_id, edge in graph.neighbours(v_id):
            if v_id < n_id:
                v1 = new_graph.get_vertex(hash(Vertex(*(R @ (np.array([v.x, v.y]) - t)))))
                v2 = new_graph.get_vertex(
                    hash(Vertex(*(R @ (np.array([graph.get_vertex(n_id).x, graph.get_vertex(n_id).y]) - t)))))
                if v1 and v2:
                    new_graph.insert_edge(v1, v2, edge)
                new_graph.insert_edge(v2, v1, edge)

    return new_graph


def count_matching_vertices(graph1, graph2, eps):
    matched = 0
    used = set()
    for v1_id in graph1.vertices():
        v1 = graph1.get_vertex(v1_id)
        for v2_id in graph2.vertices():
            if v2_id in used:
                continue
            v2 = graph2.get_vertex(v2_id)
            dist = math.hypot(v1.x - v2.x, v1.y - v2.y)
            if dist < eps:
                matched += 1
                used.add(v2_id)
                break
    return matched


def biometric_graph_registration(graph1, graph2, Ni=10, eps=3):
    edge_pairs = []

    for v1_id in graph1.vertices():
        for n1_id, _ in graph1.neighbours(v1_id):
            vec1, _, _ = edge_vector(graph1, v1_id, n1_id)
            for v2_id in graph2.vertices():
                for n2_id, _ in graph2.neighbours(v2_id):
                    vec2, _, _ = edge_vector(graph2, v2_id, n2_id)
                    angle = angle_between_vectors(vec1, vec2)
                    edge_pairs.append((angle, (v1_id, n1_id), (v2_id, n2_id)))

    edge_pairs.sort(key=lambda x: x[0])
    best_dk = float('inf')
    best_match = None

    for i in range(min(Ni, len(edge_pairs))):
        _, (g1v1, g1v2), (g2v1, g2v2) = edge_pairs[i]

        tg1 = transform_graph(graph1, graph1.get_vertex(g1v1), graph1.get_vertex(g1v2))
        tg2 = transform_graph(graph2, graph2.get_vertex(g2v1), graph2.get_vertex(g2v2))

        C = count_matching_vertices(tg1, tg2, eps)
        dk = 1 - (C / max(len(tg1.vertices()), len(tg2.vertices())))

        if dk < best_dk:
            best_dk = dk
            best_match = (tg1, tg2)

    return best_match


def main():
    data_path = "./Images"
    img_level = "easy"
    img_list = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]

    input_data = []
    for img_name in img_list:
        if img_name[-3:] == "png":
            if img_name.split('_')[-2] == img_level:
                print("Processing ", img_name, "...")

                img = cv2.imread(os.path.join(data_path, img_name))
                img_1ch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, img_bin = cv2.threshold(img_1ch, 127, 255, cv2.THRESH_BINARY)

                graph = ListGraph()
                fill_biometric_graph_from_image(img_bin, graph)
                unclutter_biometric_graph(graph)
                merge_near_vertices(graph, thr=5)

                input_data.append((img_name, graph))
                print("Saved!")

    for i in range(len(input_data)):
        for j in range(len(input_data)):
            graph1_input = input_data[i][1]
            graph2_input = input_data[j][1]

            graph1, graph2 = biometric_graph_registration(graph1_input, graph2_input, Ni=50, eps=10)

            plt.figure()
            graph1.plot_graph(v_color='red', e_color='green')

            graph2.plot_graph(v_color='gold', e_color='blue')
            plt.title('Graph comparison')
            plt.show()


if __name__ == "__main__":
    main()
