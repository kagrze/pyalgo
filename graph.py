class Graph:
    """Adjacency-list representation of a graph"""
    def __init__(self, vertex_number):
        self.__adjacencies = [[] for i in range(vertex_number)]

    def add_edge(self, a, b):
        self.__adjacencies[a].append(b)
        self.__adjacencies[b].append(a)

    def adjacencies(self, vertex):
        return self.__adjacencies[vertex]

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


def get_shortest_path_to(graph, start_vertex, target_vertex):
    """Breadth-First Search (BFS)"""
    def get_path(vertex):
        if vertex is None:
            return []
        path = get_path(edge_to[vertex])
        path.append(vertex)
        return path
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
                    return get_path(target_vertex)
                explored[adj_vertex] = True
                queue.appendleft(adj_vertex)


if __name__ == '__main__':
    """
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
    assert g.adjacencies(6) == []

    assert has_path_to(g, 3, 2)
    assert has_path_to(g, 0, 5)
    assert not has_path_to(g, 3, 6)

    assert get_shortest_path_to(g, 3, 1) == [3, 0, 1]
    sp05 = get_shortest_path_to(g, 0, 5)
    assert sp05 == [0, 1, 5] or sp05 == [0, 4, 5]
    sp32 = get_shortest_path_to(g, 3, 2)
    assert sp32 == [3, 0, 1, 2] or sp32 == [3, 4, 5, 2]
    assert not get_shortest_path_to(g, 0, 6)

    print('All tests passed')
