# Install pyvis if you don't have it
# pip install pyvis

import networkx as nx
from pyvis.network import Network


def visualize_model(m_battery):

    # Create a bipartite graph: variables ↔ constraints
    G = nx.Graph()

    # Add constraint nodes
    for cname, constraint in m_battery.constraints.items():
        G.add_node(cname, label=cname, color='orange', shape='box', title='Constraint')

        # Add variable nodes connected to the constraint
        for var in constraint.keys():
            G.add_node(var.name, label=var.name, color='lightblue', shape='ellipse', title=f'Variable ({var.cat})')
            G.add_edge(cname, var.name)

    # Initialize PyVis network
    net = Network(height="800px", width="100%", notebook=True)
    net.from_nx(G)

    # Optional: physics layout for better separation
    net.show_buttons(filter_=['physics'])
    net.show("battery_model.html")