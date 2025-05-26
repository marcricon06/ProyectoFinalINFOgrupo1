from graph import *
from node import *
import os
import matplotlib.pyplot as plt


# Function to create the first graph example
def CreateGraph_1():
    G = Graph()

    # Adding nodes to the graph
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))

    # Adding segments between the nodes
    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")

    return G


# Function to create the second graph example
def CreateGraph_2():
    G2 = Graph()

    # Adding nodes to the second graph (with different coordinates and structure)
    AddNode(G2, Node("A", 1, 20))
    AddNode(G2, Node("B", 8, 12))
    AddNode(G2, Node("C", 10, 18))
    AddNode(G2, Node("D", 12, 8))
    AddNode(G2, Node("E", 5, 3))
    AddNode(G2, Node("F", 9, 2))
    AddNode(G2, Node("G", 15, 14))
    AddNode(G2, Node("H", 17, 10))
    AddNode(G2, Node("I", 19, 3))
    AddNode(G2, Node("J", 14, 5))

    # Adding segments between the nodes (distinct connections)
    AddSegment(G2, "AB", "A", "B")
    AddSegment(G2, "BC", "B", "C")
    AddSegment(G2, "CD", "C", "D")
    AddSegment(G2, "DE", "D", "E")
    AddSegment(G2, "EF", "E", "F")
    AddSegment(G2, "FG", "F", "G")
    AddSegment(G2, "GH", "G", "H")
    AddSegment(G2, "HI", "H", "I")
    AddSegment(G2, "IJ", "I", "J")
    AddSegment(G2, "JA", "J", "A")

    return G2


# Function to test graph from a file
def test_graph_from_file():
    # Create a temporary file with graph data
    filename = "temp_graph.txt"
    with open(filename, 'w') as f:
        f.write("NODE A 0 0\n")
        f.write("NODE B 1 1\n")
        f.write("NODE C 2 2\n")
        f.write("SEGMENT AB A B\n")
        f.write("SEGMENT BC B C\n")

    g = GraphFromFile(filename)

    # Assertions to check the graph
    assert len(g.nodes) == 3
    assert len(g.segments) == 2

    names = sorted([node.name for node in g.nodes])
    assert names == ["A", "B", "C"]

    seg_names = sorted([seg.name for seg in g.segments])
    assert seg_names == ["AB", "BC"]

    os.remove(filename)
    print("test_graph_from_file passed!")


# Optional: Testing CreateGraph_1 and CreateGraph_2
if __name__ == "__main__":
    print("Probando el primer grafo...")
    G = CreateGraph_1()
    Plot(G)
    PlotNode(G, "C")
    n = GetClosest(G, 15, 5)
    print(n.name)
    n = GetClosest(G, 8, 19)
    print(n.name)

    # Ensure the first plot is shown
    plt.show()

    print("Generando el segundo grafo...")
    G2 = CreateGraph_2()
    Plot(G2)
    PlotNode(G2, "C")
    n = GetClosest(G2, 15, 5)
    print(n.name)
    n = GetClosest(G2, 8, 19)
    print(n.name)

    # Ensure the second plot is shown
    plt.show()

    # Running the graph file test
    test_graph_from_file()
