import networkx as nx
from location_manager import LocationManager

def find_shortest_path(location_manager, start_location_name, end_location_name):
    G = nx.Graph()

    # Add nodes (locations)
    for location in location_manager.locations:
        G.add_node(location.name)

    # Add edges (links between locations)
    for location in location_manager.locations:
        for link, _ in location.links:
            G.add_edge(location.name, link.name)

    try:
        shortest_path = nx.shortest_path(G, source=start_location_name, target=end_location_name)
        return shortest_path
    except nx.NetworkXNoPath:
        return None

# Example usage:
if __name__ == "__main__":
    location_manager = LocationManager()
    location_manager.load_locations()

    start_location_name = "Robotics Lab"  # Example start location
    end_location_name = "Games Academy"    # Example end location

    shortest_path = find_shortest_path(location_manager, start_location_name, end_location_name)
    output_path = ""
    if shortest_path:
        for num in range(len(shortest_path)):
            output_path += shortest_path[num]
            if num < len(shortest_path) - 1:
                method_of_travel = location_manager.find_location(shortest_path[num]).find_link_type(location_manager.find_location(shortest_path[num+1]))
                if method_of_travel != "":
                    output_path += (" (" + location_manager.find_location(shortest_path[num]).find_link_type(location_manager.find_location(shortest_path[num+1])) + ")")
                output_path += " -> "
        print("Route:", output_path)
    else:
        print("No path found.")
