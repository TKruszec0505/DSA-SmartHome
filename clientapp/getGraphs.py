import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation  # <- tu jest poprawka
import config

def network_status():
    network_topology = [
        ("comp1","server"),
        ("comp2","server"),
        ("website","server"),
        ("server","motherboard"),
        ("motherboard","mod1"),
        ("motherboard","mod2"),
    ]

    g = nx.Graph()
    g.add_edges_from(network_topology)
    pos = nx.spring_layout(g, seed=42)

    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()
        topology = network_topology.copy()
        if not config.server_is_connected:
            topology = [e for e in topology if e != ("server","motherboard")]
        if not config.website_is_connected:
            topology = [e for e in topology if e != ("website","server")]
        if not config.comp1_is_connected:
            topology = [e for e in topology if e != ("comp1","server")]
        if not config.mod1_is_connected:
            topology = [e for e in topology if e != ("motherboard","mod1")]
        if not config.mod2_is_connected:
            topology = [e for e in topology if e != ("motherboard","mod2")]

        g.clear()
        g.add_edges_from(topology)

        node_colors = []
        for node in g.nodes():
            if node == "server" and not config.server_is_connected:
                node_colors.append("red")
            elif node == "website" and not config.website_is_connected:
                node_colors.append("red")
            elif node == "comp1" and not config.comp1_is_connected:
                node_colors.append("red")
            elif node == "mod1" and not config.mod1_is_connected:
                node_colors.append("red")
            elif node == "mod2" and not config.mod2_is_connected:
                node_colors.append("red")
            else:
                node_colors.append("green")

        edge_colors = []
        for u, v in g.edges():
            if (u == "server" and v == "motherboard" and not config.server_is_connected) or \
                    (u == "website" and v == "server" and not config.website_is_connected) or \
                    (u == "comp1" and v == "server" and not config.comp1_is_connected) or \
                    (u == "motherboard" and v == "mod1" and not config.mod1_is_connected) or \
                    (u == "motherboard" and v == "mod2" and not config.mod2_is_connected):
                edge_colors.append("red")
            else:
                edge_colors.append("green")

        nx.draw(
            g,
            pos=pos,
            with_labels=True,
            ax=ax,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=800,
            font_weight='bold'
        )

    ani = FuncAnimation(fig, update, interval=500)
    plt.show()

