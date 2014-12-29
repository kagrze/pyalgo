class Graph:
    """Adjacency-list representation of a graph"""
    def __init__(self, vertex_number):
        self.__adjacencies = [{} for i in range(vertex_number)]

    def add_edge(self, a, b, length=1, undirected=True):
        self.__adjacencies[a][b] = length
        if undirected:
            self.__adjacencies[b][a] = length

    def adjacencies(self, vertex, with_length=False):
        return self.__adjacencies[vertex] if with_length else self.__adjacencies[vertex].keys()

    def get_vertex_number(self):
        return len(self.__adjacencies)


def has_path_to(graph, start_vertex, target_vertex):
    """Depth-First Search (DFS)"""
    def nested(current_vertex, explored):
        explored[current_vertex] = True
        if current_vertex == target_vertex:
            return True
        for adj_vertex in graph.adjacencies(current_vertex):
            if not explored[adj_vertex] and nested(adj_vertex, explored):
                return True
        return False
    return nested(start_vertex, [False] * graph.get_vertex_number())


def get_path(vertex, previous):
        if vertex is None:
            return []
        path = get_path(previous[vertex], previous)
        path.append(vertex)
        return path


def get_shortest_path_to(graph, start_vertex, target_vertex):
    """Breadth-First Search (BFS)"""
    from collections import deque
    queue = deque()
    queue.appendleft(start_vertex)
    explored = [False] * graph.get_vertex_number()
    explored[start_vertex] = True
    edge_to = [None] * graph.get_vertex_number()
    while len(queue) != 0:
        current_vertex = queue.pop()
        for adj_vertex in graph.adjacencies(current_vertex):
            if not explored[adj_vertex]:
                edge_to[adj_vertex] = current_vertex
                if adj_vertex == target_vertex:
                    return get_path(target_vertex, edge_to)
                explored[adj_vertex] = True
                queue.appendleft(adj_vertex)


def build_mst(graph):
    """Prim's MST algorithm; eager implementation"""
    from heap import Heap

    start_vertex = 0  # does not matter where we start building MST
    to_explore = Heap()  # values are vertex ids; keys are distances from the tree to the vertices
    to_explore.push(0, start_vertex)
    mst = []
    mst_edges = []
    previous = [None] * graph.get_vertex_number()  # previous vertex in the tree
    while to_explore.size() > 0:
        _, current_vertex = to_explore.pop()
        mst_edges.append(current_vertex)
        if previous[current_vertex] is not None:
            mst.append((previous[current_vertex], current_vertex) if previous[current_vertex] < current_vertex else (current_vertex, previous[current_vertex]))
        for adj_vertex, edge_length in graph.adjacencies(current_vertex, True).items():
            if adj_vertex in mst_edges:
                continue
            adj_length = to_explore.get_key(adj_vertex)
            if not adj_length:
                to_explore.push(edge_length, adj_vertex)
                previous[adj_vertex] = current_vertex
            elif edge_length < adj_length:
                to_explore.decrease_key(edge_length, adj_vertex)
                previous[adj_vertex] = current_vertex
    return set(mst)


def get_dijkstra_shortest_path_to(graph, start_vertex, target_vertex):
    """Dijkstra's shortest-path algorithm
    All edges are assumed to be non-negative
    The graph is assumed to be directed"""
    import sys
    from heap import Heap

    to_explore = Heap()
    to_explore.push(0, start_vertex)
    dist_to = [sys.maxsize] * graph.get_vertex_number()
    dist_to[start_vertex] = 0
    previous = [None] * graph.get_vertex_number()  # previous vertex on the path

    while to_explore.size() > 0:
        _, current_vertex = to_explore.pop()
        for adj_vertex, edge_length in graph.adjacencies(current_vertex, True).items():
            distance_through_current = dist_to[current_vertex] + edge_length
            if distance_through_current < dist_to[adj_vertex]:
                # relax a vertex
                dist_to[adj_vertex] = distance_through_current
                previous[adj_vertex] = current_vertex
                if to_explore.get_key(adj_vertex) is not None:
                    to_explore.decrease_key(distance_through_current, adj_vertex)
                else:
                    to_explore.push(distance_through_current, adj_vertex)
    return get_path(target_vertex, previous), dist_to[target_vertex]


if __name__ == '__main__':
    """
    Not connected undirected graph with fixed length of edges:

      0---1---2
     /\   \  /
    /  \   \/
    3---4---5   6
    """
    g = Graph(7)

    assert g.get_vertex_number() == 7

    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(0, 3)
    g.add_edge(0, 4)
    g.add_edge(1, 5)
    g.add_edge(2, 5)

    assert set(g.adjacencies(5)) == set([1, 2, 4])
    assert len(g.adjacencies(6)) == 0

    assert has_path_to(g, 3, 2)
    assert has_path_to(g, 0, 5)
    assert not has_path_to(g, 3, 6)

    assert get_shortest_path_to(g, 3, 1) == [3, 0, 1]
    sp05 = get_shortest_path_to(g, 0, 5)
    assert sp05 == [0, 1, 5] or sp05 == [0, 4, 5]
    sp32 = get_shortest_path_to(g, 3, 2)
    assert sp32 == [3, 0, 1, 2] or sp32 == [3, 4, 5, 2]
    assert not get_shortest_path_to(g, 0, 6)

    """
    Connected undirected graph with varying length of edges:

    0----1----4
    | \ /|
    |  2 |
    | /  |
    3---/
    """
    g = Graph(5)

    g.add_edge(0, 1, 4)
    g.add_edge(0, 3, 3)
    g.add_edge(0, 2, 1)
    g.add_edge(2, 1, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 1, 3)
    g.add_edge(1, 4, 4)

    assert build_mst(g) == set([(0, 2), (1, 2), (2, 3), (1, 4)])

    assert get_dijkstra_shortest_path_to(g, 0, 1) == ([0, 2, 1], 2)
    assert get_dijkstra_shortest_path_to(g, 3, 4) == ([3, 2, 1, 4], 6)

    """
    Connected undirected graph with varying length of edges:

      5   5
    0---1---2
     \_____/
        9
    """
    g = Graph(3)

    g.add_edge(0, 1, 5)
    g.add_edge(1, 2, 5)
    g.add_edge(2, 0, 9)

    assert build_mst(g) == set([(0, 1), (1, 2)])

    assert get_dijkstra_shortest_path_to(g, 0, 2) == ([0, 2], 9)
    assert get_dijkstra_shortest_path_to(g, 2, 0) == ([2, 0], 9)

    """
    Directed graph with varying length of edges:

      /--->---\
     /         \
    0-->--1-->--2
     \         /
      \---<---/
    """
    g = Graph(3)

    g.add_edge(0, 2, 10, undirected=False)
    g.add_edge(0, 1, 4, undirected=False)
    g.add_edge(1, 2, 4, undirected=False)
    g.add_edge(2, 0, 10, undirected=False)

    assert get_dijkstra_shortest_path_to(g, 0, 2) == ([0, 1, 2], 8)
    assert get_dijkstra_shortest_path_to(g, 2, 0) == ([2, 0], 10)

    print('All tests passed')
