import tkinter as tk
from tkinter import filedialog, messagebox
from graph import *
from node import *
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithms import Reachable, AStar
from path import PlotPath
from tkinter import simpledialog
from airspace import *
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import simplekml #Hay que instalarlo en la terminal


# Example graph from step 3
def example_graph_1():
    g = Graph()
    AddNode(g, Node("A", 1, 20))
    AddNode(g, Node("B", 8, 17))
    AddNode(g, Node("C", 15, 20))
    AddNode(g, Node("D", 18, 15))
    AddNode(g, Node("E", 2, 4))
    AddNode(g, Node("F", 6, 5))
    AddNode(g, Node("G", 12, 12))
    AddNode(g, Node("H", 10, 3))
    AddNode(g, Node("I", 19, 1))
    AddNode(g, Node("J", 13, 5))
    AddNode(g, Node("K", 3, 15))
    AddNode(g, Node("L", 4, 10))

    AddSegment(g, "AB", "A", "B")
    AddSegment(g, "AE", "A", "E")
    AddSegment(g, "AK", "A", "K")
    AddSegment(g, "BA", "B", "A")
    AddSegment(g, "BC", "B", "C")
    AddSegment(g, "BF", "B", "F")
    AddSegment(g, "BK", "B", "K")
    AddSegment(g, "BG", "B", "G")
    AddSegment(g, "CD", "C", "D")
    AddSegment(g, "CG", "C", "G")
    AddSegment(g, "DG", "D", "G")
    AddSegment(g, "DH", "D", "H")
    AddSegment(g, "DI", "D", "I")
    AddSegment(g, "EF", "E", "F")
    AddSegment(g, "FL", "F", "L")
    AddSegment(g, "GB", "G", "B")
    AddSegment(g, "GF", "G", "F")
    AddSegment(g, "GH", "G", "H")
    AddSegment(g, "ID", "I", "D")
    AddSegment(g, "IJ", "I", "J")
    AddSegment(g, "JI", "J", "I")
    AddSegment(g, "KA", "K", "A")
    AddSegment(g, "KL", "K", "L")
    AddSegment(g, "LK", "L", "K")
    AddSegment(g, "LF", "L", "F")
    return g

# Example invented graph
def example_graph_2():
    g = Graph()
    AddNode(g, Node("X", 0, 0))
    AddNode(g, Node("Y", 1, -1))
    AddNode(g, Node("Z", 2, 1))
    AddSegment(g, "XY", "X", "Y")
    AddSegment(g, "YZ", "Y", "Z")
    AddSegment(g, "ZX", "Z", "X")
    return g

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Viewer")
        self.current_graph = None
        self.reachable_nodes = set()
        self.highlighted_paths = []  # Lista de paths a destacar
        self.highlighted_neighbors = set()  # Nodos vecinos resaltados
        self.aircraft_fuel_consumption = {
            "Airbus A320": 2.5,  # litros/km
            "Boeing 737": 2.8,
            "Cessna 172": 0.12} #Consumo de los aviones

        # FRAME IZQUIERDO: botones
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # FRAME DERECHO: mapa
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones en el lado izquierdo
        tk.Button(self.left_frame, text="Show Example Graph 1", command=self.load_example_1).pack(pady=5)
        tk.Button(self.left_frame, text="Show Example Graph 2", command=self.load_example_2).pack(pady=5)
        tk.Button(self.left_frame, text="Load Graph from File", command=self.load_from_file).pack(pady=5)
        tk.Button(self.left_frame, text="Load Airspace Catalonia",command=lambda: self.load_airspace_from_folder("Cat")).pack(pady=5)
        tk.Button(self.left_frame, text="Load Airspace Spain",command=lambda: self.load_airspace_from_folder("Esp")).pack(pady=5)
        tk.Button(self.left_frame, text="Load Airspace Europe", command=lambda: self.load_airspace_from_folder("Eu")).pack(pady=5)
        tk.Button(self.left_frame, text="New Graph", command=self.new_graph).pack(pady=5)
        tk.Button(self.left_frame, text="Save Graph to File", command=self.save_graph).pack(pady=5)
        tk.Button(self.left_frame, text="Add Segment", command=self.add_segment_gui).pack(pady=5)
        tk.Button(self.left_frame, text="Add Node", command=self.add_node_gui).pack(pady=5)
        tk.Button(self.left_frame, text="Delete Node", command=self.delete_node_gui).pack(pady=5)
        tk.Button(self.left_frame, text="Show Reachable Nodes", command=self.show_reachable_nodes).pack(pady=5)
        tk.Button(self.left_frame, text="Find Shortest Path", command=self.find_shortest_path).pack(pady=5)

        self.node_var = tk.StringVar(self.root)
        self.node_dropdown = tk.OptionMenu(self.left_frame, self.node_var, "")
        self.node_dropdown.pack(pady=5)

        tk.Button(self.left_frame, text="Show Node Neighbors", command=self.show_neighbors).pack(pady=5)
        # Menús desplegables para aeropuertos
        tk.Label(self.left_frame, text="Departure Airport:").pack(pady=2)
        self.departure_airport_var = tk.StringVar(self.root)
        self.departure_airport_dropdown = tk.OptionMenu(self.left_frame, self.departure_airport_var, "")
        self.departure_airport_dropdown.pack(pady=2)

        tk.Label(self.left_frame, text="Arrival Airport:").pack(pady=2)
        self.arrival_airport_var = tk.StringVar(self.root)
        self.arrival_airport_dropdown = tk.OptionMenu(self.left_frame, self.arrival_airport_var, "")
        self.arrival_airport_dropdown.pack(pady=2)

        tk.Button(self.left_frame, text="Find Route Between Airports", command=self.find_route_between_airports).pack(
            pady=5)
        tk.Button(self.left_frame, text="Export to KML", command=self.export_to_kml).pack(pady=5)

        self.setup_canvas()

    def on_click(self, event): #añadir nodos haciendo click en el grafo
        if event.button == MouseButton.LEFT and self.current_graph is not None:
            name = f"N{len(self.current_graph.nodes) + 1}"
            new_node = Node(name, event.xdata, event.ydata)
            AddNode(self.current_graph, new_node)
            self.update_node_menu()
            self.redraw()

    def setup_canvas(self):
        # Marco para organizar la interfaz (izquierda y derecha)
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Crear figura y canvas en el frame derecho
        self.fig, self.ax = plt.subplots(figsize=(20, 18))  # Tamaño grande del mapa
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Añadir barra de herramientas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.right_frame)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Conectar eventos
        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.canvas.mpl_connect("button_press_event", self.on_click)



    def update_node_menu(self): #actualización del menu
        if not self.current_graph:
            return
        menu = self.node_dropdown["menu"]
        menu.delete(0, "end")
        for node in self.current_graph.nodes:
            menu.add_command(label=node.name, command=lambda name=node.name: self.node_var.set(name))
        if self.current_graph.nodes:
            self.node_var.set(self.current_graph.nodes[0].name)

    def redraw(self):
        if self.current_graph is None:
            return

        self.ax.clear()

        # Dibujamos segmentos
        for segment in self.current_graph.segments:
            ox, oy = segment.origin.x, segment.origin.y
            dx, dy = segment.destination.x, segment.destination.y

            self.ax.annotate("",
                             xy=(dx, dy), xytext=(ox, oy),
                             arrowprops=dict(
                                 arrowstyle="-|>",
                                 color="grey",
                                 lw=1,
                                 shrinkA=8, shrinkB=8
                             )
                             )

            dist = Distance(segment.origin, segment.destination)
            mid_x = (ox + dx) / 2
            mid_y = (oy + dy) / 2
            self.ax.text(mid_x, mid_y, f"{dist:.2f}", color="blue", fontsize=3)

        # Dibujamos nodos, coloreando vecinos en rojo, nodos alcanzables en verde, y el resto azul
        selected_node_name = self.node_var.get() if self.node_var else None

        for node in self.current_graph.nodes:
            if node.name == selected_node_name:
                color = 'darkred'  # Nodo seleccionado
            elif node.name in self.highlighted_neighbors:
                color = 'orange'  # Vecinos resaltados
            elif node.name in self.reachable_nodes:
                color = 'green'  # Nodos alcanzables
            else:
                color = 'blue'  # Otros nodos

            self.ax.plot(node.x, node.y, 'o', label=node.name, markersize=5, color=color)
            self.ax.text(node.x + 0.1, node.y + 0.1, node.name, fontsize=6)

        # Dibujamos rutas resaltadas (paths)
        for path in self.highlighted_paths:
            path_nodes = path.nodes
            xs = [n.x for n in path_nodes]
            ys = [n.y for n in path_nodes]
            self.ax.plot(xs, ys, color='red', linewidth=2, label='Highlighted Path')

        self.ax.set_aspect('equal')
        self.ax.tick_params(axis='both', which='both', length=5, labelsize=8)
        self.ax.grid(True, linestyle='--', alpha=0.5)

        self.canvas.draw()

    def load_example_1(self):#cargar ejemplos predeterminados
        self.current_graph = example_graph_1()
        self.update_node_menu()
        self.redraw()
        self.update_airport_menus()

    def load_example_2(self):
        self.current_graph = example_graph_2()
        self.update_node_menu()
        self.redraw()
        self.update_airport_menus()

    def load_from_file(self):
        filename = filedialog.askopenfilename(title="Select Graph File", filetypes=[("Text Files", "*.txt")])
        if filename:
            try:
                self.current_graph = GraphFromFile(filename)
                self.update_node_menu()
                self.redraw()
                self.update_airport_menus()

            except Exception as e: #en caso de error se muestra el mensaje
                messagebox.showerror("Error", f"Failed to load graph: {e}")

    def save_graph(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:    #para guardar el grafo actual en el dispositivo
            SaveGraphToFile(self.current_graph, filename)

    def load_airspace_from_folder(self, folder_name):
        import os
        from tkinter import messagebox
        #buscar en la carpeta data la información segun el boton que pulse
        base_path = os.path.join(os.path.dirname(__file__), 'data')
        nav_file = os.path.join(base_path, f"{folder_name}_nav")
        seg_file = os.path.join(base_path, f"{folder_name}_seg")
        aer_file = os.path.join(base_path, f"{folder_name}_aer")

        airspace = AirSpace()
        try:
            airspace.load_navpoints(nav_file)
            airspace.load_navsegments(seg_file)
            airspace.load_airports(aer_file)
        except Exception as e:
            messagebox.showerror("Error loading files", str(e))
            return

        g = Graph()
        for np in airspace.navpoints.values():
            AddNode(g, Node(np.name, np.longitude, np.latitude))  # x=lon, y=lat

        for seg in airspace.navsegments:
            origin = airspace.navpoints.get(seg.origin_number)
            dest = airspace.navpoints.get(seg.destination_number)
            if origin and dest:
                AddSegment(g, f"{origin.name}->{dest.name}", origin.name, dest.name)

        self.current_graph = g
        self.reachable_nodes = set()  # reseteamos nodos alcanzables
        self.update_node_menu()
        self.redraw()
        self.update_airport_menus()

    def new_graph(self):
        self.current_graph = Graph()
        self.highlighted_paths = []  # Limpiar rutas anteriores
        self.highlighted_neighbors = set()  # Limpiar vecinos anteriores
        self.reachable_nodes = set()  # Limpiar nodos alcanzables
        self.update_node_menu()
        self.redraw()
        self.update_airport_menus()

    def show_neighbors(self):
        if not self.current_graph or not self.node_var.get():
            return
        node_name = self.node_var.get()
        node = self.get_node_by_name(node_name)
        if not node:
            return

        # Aquí usamos node.neighbors directamente
        neighbors = set(n.name for n in node.neighbors)
        if not neighbors:
            messagebox.showinfo("Neighbors", f"No neighbors found for node {node_name}")
            return

        messagebox.showinfo("Neighbors", f"Neighbors of {node_name}: {', '.join(neighbors)}")

        self.highlighted_neighbors = neighbors
        self.highlighted_paths = []  # limpiamos rutas si estamos mostrando vecinos

        self.redraw()

    def add_node_gui(self):
        if self.current_graph is None:
            messagebox.showerror("Error", "No hay grafo cargado.")
            return

        # Ventana emergente para pedir nombre y coordenadas
        top = tk.Toplevel(self.root)
        top.title("Add Node")

        tk.Label(top, text="Node Name:").pack()
        name_entry = tk.Entry(top)
        name_entry.pack()

        tk.Label(top, text="X Coordinate:").pack()
        x_entry = tk.Entry(top)
        x_entry.pack()

        tk.Label(top, text="Y Coordinate:").pack()
        y_entry = tk.Entry(top)
        y_entry.pack()

        def on_add():
            name = name_entry.get().strip()
            try:
                x = float(x_entry.get().strip())
                y = float(y_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Las coordenadas deben ser números válidos.")
                return

            if not name:
                messagebox.showerror("Error", "El nombre del nodo no puede estar vacío.")
                return

            # Verificar que no exista un nodo con el mismo nombre
            if any(node.name == name for node in self.current_graph.nodes):
                messagebox.showerror("Error", f"Ya existe un nodo con el nombre '{name}'.")
                return

            # Añadir el nodo al grafo
            new_node = Node(name, x, y)
            AddNode(self.current_graph, new_node)

            self.update_node_menu()
            self.redraw()
            top.destroy()

        tk.Button(top, text="Add", command=on_add).pack(pady=5)

    def add_segment_gui(self):
        if not self.current_graph:
            return
        top = tk.Toplevel(self.root)
        top.title("Add Segment")
        #Pedir nombre para el segmento, origen y destino
        tk.Label(top, text="Segment Name:").pack()
        name_entry = tk.Entry(top)
        name_entry.pack()

        tk.Label(top, text="Origin Node:").pack()
        origin_var = tk.StringVar(top)
        tk.OptionMenu(top, origin_var, *[n.name for n in self.current_graph.nodes]).pack()

        tk.Label(top, text="Destination Node:").pack()
        dest_var = tk.StringVar(top)
        tk.OptionMenu(top, dest_var, *[n.name for n in self.current_graph.nodes]).pack()

        def on_add():
            AddSegment(self.current_graph, name_entry.get(), origin_var.get(), dest_var.get())
            self.redraw()
            top.destroy()

        tk.Button(top, text="Add", command=on_add).pack()

    def delete_node_gui(self): #Eliminar el nodo seleccionado
        if not self.current_graph:
            return
        name = self.node_var.get()
        DeleteNode(self.current_graph, name)
        self.update_node_menu()
        self.redraw()

    def show_reachable_nodes(self):
        if not self.current_graph or not self.node_var.get():
            return

        node = next((n for n in self.current_graph.nodes if n.name == self.node_var.get()), None)
        if node:
            reachable = Reachable(self.current_graph, node)
            self.reachable_nodes = set(n.name for n in reachable)

            reachable_names = [n.name for n in reachable]
            messagebox.showinfo("Reachable Nodes", f"Nodes reachable from {node.name}: {', '.join(reachable_names)}")
            self.redraw()

    def find_shortest_path(self):
        if not self.current_graph or not self.node_var.get():
            return

        start_node_name = self.node_var.get()
        destination_name = simpledialog.askstring("Select Destination", "Enter destination node name:")

        start_node = next((n for n in self.current_graph.nodes if n.name == start_node_name), None)
        destination_node = next((n for n in self.current_graph.nodes if n.name == destination_name), None)

        if start_node and destination_node:
            path = AStar(self.current_graph, start_node, destination_node)
            if path:
                path_names = [n.name for n in path.nodes]
                messagebox.showinfo("Shortest Path", f"Shortest path: {' -> '.join(path_names)}")

                # Guardamos la ruta para dibujar y exportar
                self.highlighted_paths = [path]
                self.highlighted_neighbors = set()  # limpiamos vecinos al mostrar ruta

                self.redraw()
                PlotPath(self.ax, path)
                self.canvas.draw()
            else:
                messagebox.showinfo("No Path", "No path found between the nodes.")
        else:
            messagebox.showerror("Error", "Invalid start or destination node.")

    def update_airport_menus(self):
        if not self.current_graph:
            return

        airport_codes = sorted({
            node.name.split('.')[0]
            for node in self.current_graph.nodes
            if node.name.endswith('.D') or node.name.endswith('.A')
        })

        dep_menu = self.departure_airport_dropdown["menu"]
        dep_menu.delete(0, "end")
        for code in airport_codes:
            dep_menu.add_command(label=code, command=lambda value=code: self.departure_airport_var.set(value))

        arr_menu = self.arrival_airport_dropdown["menu"]
        arr_menu.delete(0, "end")
        for code in airport_codes:
            arr_menu.add_command(label=code, command=lambda value=code: self.arrival_airport_var.set(value))

        if airport_codes:
            self.departure_airport_var.set(airport_codes[0])
            self.arrival_airport_var.set(airport_codes[0])

    def get_node_by_name(self, name):
        for node in self.current_graph.nodes:
            if node.name == name:
                return node
        return None

    def show_aircraft_options(self, path):
        top = tk.Toplevel(self.root)
        top.title("Elige un avión")

        tk.Label(top, text="Selecciona un avión para calcular el combustible:").pack(pady=10)

        def calculate_fuel(aircraft):
            total_distance = sum(
                Distance(path.nodes[i], path.nodes[i + 1]) for i in range(len(path.nodes) - 1)
            )
            fuel_used = total_distance * self.aircraft_fuel_consumption[aircraft]
            messagebox.showinfo("Combustible estimado",
                                f"{aircraft} necesitará aproximadamente {fuel_used:.2f} litros de combustible para recorrer el camino.")
            top.destroy()

        for aircraft in self.aircraft_fuel_consumption:
            tk.Button(top, text=aircraft, command=lambda a=aircraft: calculate_fuel(a)).pack(pady=2)

        tk.Button(top, text="No lo necesito", command=top.destroy).pack(pady=10)

    def find_route_between_airports(self):
        dep_airport = self.departure_airport_var.get()
        arr_airport = self.arrival_airport_var.get()

        departure_node_name = f"{dep_airport}.D"
        arrival_node_name = f"{arr_airport}.A"

        if not self.current_graph:
            messagebox.showerror("Error", f"No graph loaded.")
            return

        start_node = self.get_node_by_name(departure_node_name)
        end_node = self.get_node_by_name(arrival_node_name)

        if start_node is None or end_node is None:
            messagebox.showerror("Error", f"No nodes found for selected airports.")
            return

        path = AStar(self.current_graph, start_node, end_node)
        if path:
            path_names = [n.name for n in path.nodes]
            messagebox.showinfo("Route Found", f"Path: {' -> '.join(path_names)}")

            # Guardamos la ruta para dibujar y exportar
            self.highlighted_paths = [path]
            self.highlighted_neighbors = set()  # limpiamos vecinos al mostrar ruta

            self.redraw()
            PlotPath(self.ax, path)
            self.canvas.draw()
            self.show_aircraft_options(path)

        else:
            messagebox.showinfo("No Path", f"No path found from {departure_node_name} to {arrival_node_name}")

    def export_to_kml(self):

        if not self.current_graph:
            messagebox.showerror("Error", "No hay grafo cargado.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".kml",
                                                 filetypes=[("KML files", "*.kml")])
        if not file_path:
            return

        kml = simplekml.Kml()

        # Crear puntos (nodos)
        for node in self.current_graph.nodes:
            pnt = kml.newpoint(name=node.name, coords=[(node.x, node.y)])
            if node.name in self.highlighted_neighbors:
                pnt.style.iconstyle.color = simplekml.Color.red  # vecinos en rojo
            elif node.name in self.reachable_nodes:
                pnt.style.iconstyle.color = simplekml.Color.green  # nodos alcanzables en verde
            else:
                pnt.style.iconstyle.color = simplekml.Color.blue  # normal azul

        # Crear líneas (segmentos)
        for segment in self.current_graph.segments:
            line = kml.newlinestring(name=f"{segment.origin.name} - {segment.destination.name}",
                                     coords=[(segment.origin.x, segment.origin.y),
                                             (segment.destination.x, segment.destination.y)])
            line.style.linestyle.color = simplekml.Color.gray
            line.style.linestyle.width = 2

        # Crear líneas para las rutas resaltadas (paths)
        for path in self.highlighted_paths:
            coords = [(n.x, n.y) for n in path.nodes]
            route_line = kml.newlinestring(name="Highlighted Path", coords=coords)
            route_line.style.linestyle.color = simplekml.Color.red
            route_line.style.linestyle.width = 4

        kml.save(file_path)
        messagebox.showinfo("Exportación Exitosa", f"Grafo exportado a {file_path}")


# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()



