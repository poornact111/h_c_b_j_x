import tkinter as tk
from tkinter import simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra's Algorithm Visualizer")

        self.graph = nx.Graph()
        self.node_positions = {}
        self.selected_node = None

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.add_node_button = tk.Button(self.frame, text="Add Node", command=self.add_node)
        self.add_node_button.pack(side=tk.LEFT)

        self.add_edge_button = tk.Button(self.frame, text="Add Edge", command=self.start_edge_creation)
        self.add_edge_button.pack(side=tk.LEFT)

        self.shortest_path_button = tk.Button(self.frame, text="Find Shortest Path", command=self.find_shortest_path)
        self.shortest_path_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.frame, text="Clear", command=self.clear)
        self.clear_button.pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.canvas_click)

    def add_node(self):
        node = simpledialog.askstring("Input", "Enter node name:")
        if node:
            self.graph.add_node(node)
            self.node_positions[node] = self.canvas_click_pos
            self.draw_graph()

    def start_edge_creation(self):
        self.selected_node = None
        messagebox.showinfo("Info", "Click on the first node to create an edge from.")

    def canvas_click(self, event):
        self.canvas_click_pos = (event.x, event.y)
        if self.selected_node is None:
            node = self.get_node_at_pos(event.x, event.y)
            if node:
                self.selected_node = node
        else:
            node = self.get_node_at_pos(event.x, event.y)
            if node and node != self.selected_node:
                weight = simpledialog.askfloat("Input", "Enter the weight of the edge:")
                if weight is not None:
                    self.graph.add_edge(self.selected_node, node, weight=weight)
                    self.selected_node = None
                    self.draw_graph()
            else:
                messagebox.showerror("Error", "Invalid selection. Please start over by clicking on 'Add Edge' button.")
                self.selected_node = None

    def get_node_at_pos(self, x, y):
        for node, (nx, ny) in self.node_positions.items():
            if (nx - x)**2 + (ny - y)**2 <= 15**2:
                return node
        return None

    def find_shortest_path(self):
        source = simpledialog.askstring("Input", "Enter the source node:")
        target = simpledialog.askstring("Input", "Enter the target node:")
        if source and target:
            try:
                path = nx.dijkstra_path(self.graph, source, target)
                length = nx.dijkstra_path_length(self.graph, source, target)
                self.draw_graph(path)
                messagebox.showinfo("Result", f"The shortest path from {source} to {target} is {path} with a total weight of {length}.")
            except nx.NetworkXNoPath:
                messagebox.showerror("Error", f"No path found between {source} and {target}.")
            except nx.NodeNotFound as e:
                messagebox.showerror("Error", str(e))

    def draw_graph(self, highlight_path=None):
        self.canvas.delete("all")
        pos = self.node_positions

        for node, (x, y) in pos.items():
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="lightblue")
            self.canvas.create_text(x, y, text=node)

        for edge in self.graph.edges(data=True):
            n1, n2, data = edge
            x1, y1 = pos[n1]
            x2, y2 = pos[n2]
            self.canvas.create_line(x1, y1, x2, y2)
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(data['weight']))

        if highlight_path:
            for i in range(len(highlight_path)-1):
                n1 = highlight_path[i]
                n2 = highlight_path[i+1]
                x1, y1 = pos[n1]
                x2, y2 = pos[n2]
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    def clear(self):
        self.graph.clear()
        self.node_positions.clear()
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraApp(root)
    root.mainloop()
