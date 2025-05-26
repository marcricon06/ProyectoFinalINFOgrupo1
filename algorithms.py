from path import Path
from node import Distance

def Reachable(graph, start_node):
    visited = set()
    stack = [start_node]

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            stack.extend(current.neighbors)

    return visited

def AStar(graph, origin, destination):
    paths = [Path([origin], 0)]

    while paths:
        # Select path with lowest estimated cost
        best = min(paths, key=lambda p: p.cost + Distance(p.LastNode(), destination))
        paths.remove(best)

        last_node = best.LastNode()

        for neighbor in last_node.neighbors:
            if best.ContainsNode(neighbor):
                continue

            new_path = Path(best.nodes[:], best.cost)
            new_path.AddNode(neighbor, Distance(last_node, neighbor))

            if neighbor == destination:
                return new_path

            # Avoid longer existing paths
            skip = False
            for p in paths:
                if p.ContainsNode(neighbor) and p.CostToNode(neighbor) <= new_path.CostToNode(neighbor):
                    skip = True
                    break
            if not skip:
                paths.append(new_path)

    return None
