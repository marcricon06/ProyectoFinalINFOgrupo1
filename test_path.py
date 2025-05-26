from node import Node
from graph import Graph, AddNode, AddSegment
from path import PlotPath
from algorithms import Reachable, AStar

# Create graph
G = Graph()
A = Node("A", 5, 6)
B = Node("B", 10, 6)
E = Node("E", 6, 1)
K = Node("K", 10, 1)
L = Node("L", 15, 1)
F = Node("F", 20, 1)

for n in [A, B, E, K, L, F]:
    AddNode(G, n)

AddSegment(G, "AB", "A", "B")
AddSegment(G, "AE", "A", "E")
AddSegment(G, "AK", "A", "K")
AddSegment(G, "KL", "K", "L")
AddSegment(G, "LF", "L", "F")

# Reachability
reachable = Reachable(G, A)
print("Reachable from A:", [n.name for n in reachable])

# A* Shortest Path
shortest = AStar(G, A, F)
if shortest:
    print("Shortest Path:", [n.name for n in shortest.nodes])
    PlotPath(G, shortest)
else:
    print("No path found")
