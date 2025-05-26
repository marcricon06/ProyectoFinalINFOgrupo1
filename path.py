
from node import Distance

class Path:
    def __init__(self, nodes=None, cost=0):
        self.nodes = nodes if nodes else []
        self.cost = cost

    def LastNode(self):
        return self.nodes[-1] if self.nodes else None

    def AddNode(self, node, cost):
        self.nodes.append(node)
        self.cost += cost

    def ContainsNode(self, node):
        return node in self.nodes

    def CostToNode(self, node):
        cost = 0
        for i in range(len(self.nodes) - 1):
            if self.nodes[i] == node:
                return cost
            cost += Distance(self.nodes[i], self.nodes[i + 1])
        return -1

def PlotPath(ax, path):
    # Ahora se usa 'ax' como el argumento para el eje donde dibujamos
    for i in range(len(path.nodes) - 1):
        ox, oy = path.nodes[i].x, path.nodes[i].y
        dx, dy = path.nodes[i+1].x, path.nodes[i+1].y
        # Dibujamos las conexiones del camino con un color diferente, por ejemplo, verde
        ax.annotate("",
                    xy=(dx, dy), xytext=(ox, oy),
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color="green",
                        lw=3,
                        shrinkA=8, shrinkB=8
                    )
                    )
    # Redibujamos el canvas
    ax.figure.canvas.draw()

