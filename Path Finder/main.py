import heapq

map = {
    'a': [('c', 3), ('f', 2)],
    'b': [('d', 1), ('e', 2), ('f', 6), ('g', 2)],
    'c': [('a', 3), ('f', 2), ('e', 1), ('d', 4)],
    'd': [('c', 4), ('b', 1)],
    'e': [('c', 1), ('f', 3), ('b', 2)],
    'f': [('a', 2), ('c', 2), ('e', 3), ('g', 5)],
    'g': [('f', 5), ('b', 2)]
}


def dijkstra(map, start, end):
    # Min-heap priority queue
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == end:
            return cost, path

        for next_node, weight in map.get(node, []):
            if next_node not in visited:
                heapq.heappush(queue, (cost + weight, next_node, path))

    return float("inf"), []


# Find the shortest path from 'a' to 'b'
time, path = dijkstra(map, 'e', 'g')

print("Path:", " -> ".join(path))
print("Total time:", time)