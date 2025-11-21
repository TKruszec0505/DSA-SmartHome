import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import config

def network_status():
    # lista wszystkich węzłów
    nodes = ["comp1", "comp2", "website", "server", "motherboard", "mod1", "mod2"]
    # lista wszystkich możliwych połączeń
    all_edges = [
        ("comp1","server"),
        ("comp2","server"),
        ("website","server"),
        ("server","motherboard"),
        ("motherboard","mod1"),
        ("motherboard","mod2"),
    ]

    g = nx.Graph()
    g.add_nodes_from(nodes)
    pos = nx.spring_layout(g, seed=42)

    fig, ax = plt.subplots()

    def update(frame):
        ax.clear()

        nodes = ["comp1", "comp2", "website", "server", "motherboard", "mod1", "mod2"]
        edges = [
            ("comp1", "server"),
            ("comp2", "server"),
            ("website", "server"),
            ("server", "motherboard"),
            ("motherboard", "mod1"),
            ("motherboard", "mod2"),
        ]

        g.clear()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)  # dodajemy WSZYSTKIE krawędzie

        # kolory węzłów
        node_colors = []
        for node in nodes:
            if (node == "server" and not config.server_is_connected) or \
                    (node == "website" and not config.website_is_connected) or \
                    (node == "comp1" and not config.comp1_is_connected) or \
                    (node == "mod1" and not config.mod1_is_connected) or \
                    (node == "mod2" and not config.mod2_is_connected):
                node_colors.append("red")
            else:
                node_colors.append("green")

        # kolory krawędzi zależnie od stanu
        edge_colors = []
        for u, v in edges:
            if (u == "server" and not config.server_is_connected) or \
                    (u == "website" and not config.website_is_connected) or \
                    (u == "comp1" and not config.comp1_is_connected) or \
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

    ani = FuncAnimation(fig, update, interval=500, cache_frame_data=False)
    plt.show()
