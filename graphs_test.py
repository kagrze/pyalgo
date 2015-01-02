from graphs import Graph, has_path_to, get_bfs_shortest_path_to
from graphs import get_dijkstra_shortest_path_to, get_bellman_ford_shortest_path_to, build_mst

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

assert get_bfs_shortest_path_to(g, 3, 1) == [3, 0, 1]
sp05 = get_bfs_shortest_path_to(g, 0, 5)
assert sp05 == [0, 1, 5] or sp05 == [0, 4, 5]
sp32 = get_bfs_shortest_path_to(g, 3, 2)
assert sp32 == [3, 0, 1, 2] or sp32 == [3, 4, 5, 2]
assert not get_bfs_shortest_path_to(g, 0, 6)

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

assert get_bellman_ford_shortest_path_to(g, 0, 1) == ([0, 2, 1], 2)
assert get_bellman_ford_shortest_path_to(g, 3, 4) == ([3, 2, 1, 4], 6)

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

assert get_bellman_ford_shortest_path_to(g, 0, 2) == ([0, 2], 9)
assert get_bellman_ford_shortest_path_to(g, 2, 0) == ([2, 0], 9)

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

assert get_bellman_ford_shortest_path_to(g, 0, 2) == ([0, 1, 2], 8)
assert get_bellman_ford_shortest_path_to(g, 2, 0) == ([2, 0], 10)

print('All tests passed')
