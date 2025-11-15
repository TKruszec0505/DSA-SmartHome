import matplotlib.pyplot as plt
import matplotlib.animation as animation
import config
import networkx as nx
import time

def network_status():

    network_topology = [("comp1","server"),
                        ("comp2","server"),
                        ("website","server"),
                        ("server","motherboard"),
                        ("motherboard","mod1"),
                        ("motherboard","mod2"),]
    def network_status_check():
        g = nx.Graph()
        g.add_edges_from(network_topology)

        pos = nx.spring_layout(g,seed=42)
        plt.ion()
        fig, ax = plt.subplots()

        while True:
            ax.clear()

            network_topology_updated = network_topology.copy()
            if not config.server_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if edge != ("server","motherboard") ]
            if not config.website_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if edge != ("website","server") ]
            if not config.comp1_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if edge != ("comp1","server") ]
            if not config.mod1_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if edge != ("motherboard","mod1") ]
            if not config.mod2_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if edge != ("motherboard","mod2") ]

            g.clear()
            g.add_edges_from(network_topology_updated)

            nx.draw(g, pos=pos, with_labels=True,ax=ax,node_color = 'skyblue', node_size = 800 ,font_weight='gray')
            plt.pause(1)
    network_status_check()