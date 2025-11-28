import matplotlib.pyplot as plt
import matplotlib.animation as animation

import time

import networkx as nx

from mainapp import config


def graph():
    K = config.volume_val
    x_data = []
    k_data = []

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)

    def init():
        ax.set_xlim(0, 50)  # zakres osi X (czas)
        ax.set_ylim(-1, 1)  # zakres osi Y (wartości K)
        return line,

    def update(frame):

        #K = random.uniform(-1, 1)

        # zapis danych
        x_data.append(time.time())
        k_data.append(K)

        # zeby wykres przesuwal sie w czasie
        if len(x_data) > 50:
            x_data.pop(0)
            k_data.pop(0)

        # aktualizacja danych na wykresie
        line.set_data(range(len(k_data)), k_data)
        return line,

    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=50, cache_frame_data=False)
    plt.show()
def network_status():
    last_serial_state = config.serial_is_connected
    network_topology = [("comp1","server"),
                        ("comp2","server"),
                        ("website","server"),
                        ("server","motherboard"),
                        ("motherboard","mod1"),
                        ("motherboard","mod2")]
    def network_status_check():
        G = nx.Graph()
        G.add_edges_from(network_topology)

        pos = nx.spring_layout(G, seed=42)  # stale pozycje
        plt.ion()
        fig, ax = plt.subplots()

        while True:
            ax.clear()


            network_topology_updated = network_topology.copy()
            if not config.serial_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if
                                            edge != ("server", "motherboard")]
            if not config.website_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if
                                            edge != ("website", "server")]
            if not config.comp2_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if
                                            edge != ("comp2","server")]
            if not config.mod2_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if
                                            edge != ("motherboard","mod2")]
            if not config.mod1_is_connected:
                network_topology_updated = [edge for edge in network_topology_updated if
                                            edge != ("motherboard","mod1")]
            G.clear()
            G.add_edges_from(network_topology_updated)

            nx.draw(G, pos=pos,
                    with_labels=True,
                    ax=ax,
                    node_color='skyblue',
                    node_size=800,
                    edge_color='gray')
            plt.pause(1)

    network_status_check()





