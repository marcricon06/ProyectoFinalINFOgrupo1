from node import *
from segment import *
import matplotlib.pyplot as plt
class Graph:
    def __init__(self):
        self.nodes=[]
        self.segments=[]
def AddNode(g,n):
    for node in g.nodes:
        if n in g.nodes:
            return False
    g.nodes.append(n)
    return True
def AddSegment(g,nameSegment, nameOrigin, nameDestination):
    origin = None
    destination = None

    for node in g.nodes:
        if node.name == nameOrigin:
            origin = node
        if node.name == nameDestination:
            destination = node

    if origin is None or destination is None:
        return False

    segment = Segment(nameSegment, origin, destination)
    g.segments.append(segment)

    AddNeighbor(origin, destination)
    return True

def GetClosest(g, x, y):
    if not g.nodes:
        return None
    return min(g.nodes, key=lambda n: Distance(n, Node("", x, y)))


def Plot(g):
    plt.figure()

    for segment in g.segments:
        x0, y0 = segment.origin.x, segment.origin.y
        x1, y1 = segment.destination.x, segment.destination.y

        dx = x1 - x0
        dy = y1 - y0

        # Dibujar flecha desde el nodo origen al nodo destino
        plt.arrow(
            x0, y0, dx * 0.85, dy * 0.85,  # Largo reducido para evitar que tape el nodo destino
            head_width=0.6, head_length=0.8,
            fc='gray', ec='gray',
            length_includes_head=True
        )

        # Mostrar el costo del segmento
        mid_x = x0 + dx * 0.5
        mid_y = y0 + dy * 0.5
        plt.text(mid_x, mid_y, str(round(segment.cost, 2)), fontsize=9, color='blue')

    # Dibujar nodos
    for node in g.nodes:
        plt.scatter(node.x, node.y, color='black', s=100, zorder=3)
        plt.text(node.x, node.y, f"{node.name}", fontsize=12, color='black', zorder=4)

    # Añadir cuadrícula para facilitar ubicación
    plt.grid(True, which='both', linestyle='--', color='red', alpha=0.3)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Grafo dirigido con flechas")
    plt.show()


def PlotNode(graph, node_name):
    node = next((n for n in graph.nodes if n.name == node_name), None)
    if not node:
        return

    # Filtrar los segmentos que conectan con el nodo
    connected_segments = [
        segment for segment in graph.segments
        if segment.origin == node or segment.destination == node
    ]

    # Dibujar los segmentos conectados
    for segment in connected_segments:
        ox, oy = segment.origin.x, segment.origin.y
        dx, dy = segment.destination.x, segment.destination.y
        plt.plot([ox, dx], [oy, dy], color='red', linestyle='-')  # Usamos color y linestyle por separado

    # Redibujar el canvas
    plt.plot(node.x, node.y, 'bo')  # Nodo en azul
    plt.text(node.x, node.y, f" {node.name}", fontsize=15)
    plt.draw()  # Dibuja en la figura actual


def GraphFromFile(filename):
    g = Graph()

    node_dict = {}  # Para buscar nodos por nombre luego

    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == "NODE":
                if len(parts) < 4:
                    raise ValueError(f"Línea de nodo inválida: {line.strip()}")
                name = parts[1]
                x = float(parts[2])
                y = float(parts[3])
                # Soporte para descripción opcional
                descripcion = " ".join(parts[4:]) if len(parts) > 4 else ""
                node = Node(name, x, y, descripcion)
                AddNode(g, node)
                node_dict[name] = node

            elif parts[0] == "SEGMENT":
                if len(parts) != 4:
                    raise ValueError(f"Línea de segmento inválida: {line.strip()}")
                seg_name = parts[1]
                origin = parts[2]
                destination = parts[3]
                AddSegment(g, seg_name, origin, destination)

    return g


def SaveGraphToFile(graph, filename):
    with open(filename, 'w') as f:
        for node in graph.nodes:
            f.write(f"NODE {node.name} {node.x} {node.y}\n")

        for segment in graph.segments:
            f.write(f"SEGMENT {segment.name} {segment.origin.name} {segment.destination.name}\n")

def DeleteNode(graph, name):
    # Buscar el nodo a eliminar
    node_to_delete = next((node for node in graph.nodes if node.name == name), None)
    if not node_to_delete:
        return  # No se encontró el nodo, salimos

    # Eliminar los segmentos relacionados con el nodo
    graph.segments = [
        segment for segment in graph.segments
        if segment.origin != node_to_delete and segment.destination != node_to_delete
    ]

    # Eliminar el nodo de la lista de nodos
    graph.nodes.remove(node_to_delete)

    # Eliminarlo también de las listas de vecinos
    for node in graph.nodes:
        if node_to_delete in node.neighbors:
            node.neighbors.remove(node_to_delete)
