import math

class Node:
    def __init__(self,name,x,y):
        self.name=name
        self.x=x
        self.y=y
        self.neighbors= []
def AddNeighbor(n1,n2):
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def Distance(n1, n2): #Calcular la distancia a partir de latitud y longitud
    R = 6371  # Radio de la Tierra en km

    lat1 = math.radians(n1.x)
    lon1 = math.radians(n1.y)
    lat2 = math.radians(n2.x)
    lon2 = math.radians(n2.y)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
