import math

import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
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


def plot_graph(self, v_color, e_color):
    for idx, v in enumerate(self.vertex):
        y, x = v.key
        plt.scatter(x, y, c=v_color)
        for n_idx, _ in self.neighbours(idx):
            yn, xn = self.getVertex(n_idx).key
            plt.plot([x, xn], [y, yn], color=e_color)


class BiometricGraph(ListGraph):
    def __init__(self):
        super().__init__()

    def fill_from_image(self, binary_image):
        rows, cols = binary_image.shape
        for y in range(rows):
            for x in range(cols):
                if binary_image[y, x] == 255:  # biały piksel
                    current_vertex = Vertex((y, x))
                    self.insert_vertex(current_vertex)
                    # sprawdzenie sąsiednich pikseli
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < rows and 0 <= nx < cols and binary_image[ny, nx] == 255:
                                neighbor_vertex = Vertex((ny, nx))
                                if hash(neighbor_vertex) not in self.vertex:
                                    self.insert_vertex(neighbor_vertex)
                                self.insert_edge(current_vertex, neighbor_vertex, None)
                                self.insert_edge(neighbor_vertex, current_vertex, None)

    def unclutter(self):
        to_remove = set()
        to_add = []

        for v_id in list(self.vertices()):
            neighbours = list(self.neighbours(v_id))
            if len(neighbours) != 2:
                for n_id, _ in neighbours:
                    path = [v_id]
                    prev_id = v_id
                    current_id = n_id
                    while len(self.neighbours(current_id)) == 2:
                        path.append(current_id)
                        n_ids = [nid for nid, _ in self.neighbours(current_id) if nid != prev_id]
                        if not n_ids:
                            break
                        prev_id, current_id = current_id, n_ids[0]
                    path.append(current_id)
                    for pid in path[1:-1]:
                        to_remove.add(pid)
                    to_add.append((v_id, current_id))

        for v in to_remove:
            self.delete_vertex(v)

        for v1, v2 in to_add:
            if v1 != v2:
                self.insert_edge(self.get_vertex(v1), self.get_vertex(v2), None)
                self.insert_edge(self.get_vertex(v2), self.get_vertex(v1), None)

    def merge_near_vertices(self, threshold=3):
        merged = []
        visited = set()

        ids = list(self.vertices())
        for i in range(len(ids)):
            if ids[i] in visited:
                continue
            group = [ids[i]]
            y1, x1 = self.get_vertex(ids[i]).key
            for j in range(i + 1, len(ids)):
                y2, x2 = self.get_vertex(ids[j]).key
                if ids[j] not in visited and math.hypot(x2 - x1, y2 - y1) < threshold:
                    group.append(ids[j])
                    visited.add(ids[j])
            merged.append(group)

        for group in merged:
            if len(group) < 2:
                continue
            new_coords = np.mean([self.get_vertex(vid).key for vid in group], axis=0)
            new_vertex = Vertex(tuple(map(int, new_coords)))
            self.insert_vertex(new_vertex)

            new_edges = set()
            for vid in group:
                for nid, _ in self.neighbours(vid):
                    if nid not in group:
                        new_edges.add(nid)
            for nid in new_edges:
                self.insert_edge(new_vertex, self.get_vertex(nid), None)
                self.insert_edge(self.get_vertex(nid), new_vertex, None)

            for vid in group:
                self.delete_vertex(vid)

    def plot(self, v_color='red', e_color='blue', Y=None):
        for idx, v in self.vertex.items():
            y, x = v.key
            if Y is not None:
                y = Y - y
            plt.scatter(x, y, c=v_color, s=10)
            for n_idx, _ in self.neighbours(idx):
                yn, xn = self.get_vertex(n_idx).key
                if Y is not None:
                    yn = Y - yn
                plt.plot([x, xn], [y, yn], color=e_color, linewidth=0.5)

    def transform(self, tx, ty, theta):
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        new_vertex = {}
        new_edges = {}

        for v_id in self.vertices():
            y, x = self.get_vertex(v_id).key
            x += tx
            y += ty
            x_rot = x * cos_t + y * sin_t
            y_rot = -x * sin_t + y * cos_t
            new_vertex[v_id] = Vertex((int(y_rot), int(x_rot)))

        for v_id in self.vertices():
            new_edges[v_id] = {}
            for n_id, val in self.neighbours(v_id):
                new_edges[v_id][n_id] = val

        self.vertex = new_vertex
        self.neighbor_list = new_edges

def biometric_graph_registration(graph1: BiometricGraph, graph2: BiometricGraph, Ni=50, eps=10):
    """
    Dopasowuje dwa grafy biometryczne przez przekształcenie (obrót i przesunięcie).
    Zwraca dwa grafy po dopasowaniu do wspólnych współrzędnych.
    """
    best_score = 0
    best_transform = None
    best_graph2_aligned = None

    edges1 = graph1.edges
    edges2 = graph2.edges

    for edge1 in edges1:
        for edge2 in edges2:
            # v1 and v2 are endpoints of edge1
            v1a, v1b = graph1.vertices[edge1[0]], graph1.vertices[edge1[1]]
            # u1 and u2 are endpoints of edge2
            v2a, v2b = graph2.vertices[edge2[0]], graph2.vertices[edge2[1]]

            # Calculate vectors
            vec1 = v1b - v1a
            vec2 = v2b - v2a

            # Compute angle between edges
            angle1 = np.arctan2(vec1[1], vec1[0])
            angle2 = np.arctan2(vec2[1], vec2[0])
            angle_diff = angle1 - angle2

            # Rotate and translate graph2
            R = np.array([[np.cos(angle_diff), -np.sin(angle_diff)],
                          [np.sin(angle_diff),  np.cos(angle_diff)]])
            t = v1a - R @ v2a

            # Apply transformation to graph2
            transformed_vertices = [R @ v + t for v in graph2.vertices]

            # Count how many transformed vertices match vertices in graph1
            matched = 0
            for tv in transformed_vertices:
                for gv in graph1.vertices:
                    if np.linalg.norm(tv - gv) < eps:
                        matched += 1
                        break

            if matched > best_score:
                best_score = matched
                best_transform = (R, t)
                best_graph2_aligned = BiometricGraph()
                best_graph2_aligned.vertices = transformed_vertices
                best_graph2_aligned.edges = graph2.edges

    # Tworzymy kopię graph1
    graph1_copy = BiometricGraph()
    graph1_copy.vertices = graph1.vertices
    graph1_copy.edges = graph1.edges

    if best_graph2_aligned is None:
        # Jeśli nie znaleziono dobrego dopasowania, zwróć oryginalne grafy
        return graph1_copy, graph2

    return graph1_copy, best_graph2_aligned

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

                graph = BiometricGraph()
                graph.fill_from_image(img_bin)
                graph.unclutter()
                graph.merge_near_vertices(5)

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
