import networkx as nx
import matplotlib.pyplot as plt
from location_manager import LocationManager

class LocationVisualizer:
    def __init__(self, locations):
        self.G = nx.Graph()

        # Add nodes (locations)
        for location in locations:
            self.G.add_node(location.name, description=location.description)

        # Add edges (links between locations)
        for location in locations:
            for linked_location, link_type in location.links:
                self.G.add_edge(location.name, linked_location.name, link_type=link_type)

        self.fig, self.ax = plt.subplots()
        self.pos = nx.kamada_kawai_layout(self.G)  # Positions for all nodes using Kamada-Kawai layout

        # Draw graph
        nx.draw(self.G, self.pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8, font_weight="bold", alpha=0.8, ax=self.ax)
        self.ax.set_title("Location Network")

        # Initialize variables for handling dragging
        self.dragging = False
        self.selected_node = None

        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        for node in self.G.nodes():
            if ((self.pos[node][0] - event.xdata)**2 + (self.pos[node][1] - event.ydata)**2) <= 0.01:
                self.selected_node = node
                self.dragging = True
                break

    def on_motion(self, event):
        if not self.dragging:
            return
        if event.inaxes != self.ax:
            return
        self.pos[self.selected_node] = [event.xdata, event.ydata]
        self.update_plot()

    def on_release(self, event):
        if not self.dragging:
            return
        self.dragging = False

    def update_plot(self):
        self.ax.clear()
        nx.draw(self.G, self.pos, with_labels=True, node_size=100, node_color="skyblue", font_size=8, font_weight="bold", alpha=0.8, ax=self.ax)
        self.ax.set_title("Location Network")
        plt.draw()


if __name__ == "__main__":
    location_manager = LocationManager()
    location_manager.load_locations()
    visualizer = LocationVisualizer(location_manager.locations)
    plt.show()
