from typing import Optional, List

import random
import numpy as np
import networkx as nx
from dataclasses import dataclass, field
from sympy import *
import matplotlib.pyplot as plt

from components import Component, Capacitor, Inductor


@dataclass
class Circuit:
    graph: nx.Graph
    components: Optional[List[Component]] = None

    def solve(self):  # caveman logic:
        # graph of nodes
        nodes = nx.line_graph(self.graph)
        # determine active nodes and passive nodes
        for n in nodes.nodes:
            neighbors = nx.neighbors(nodes, n)
            if len(set([type(self.components[i]) for i in neighbors])) > 1:
                # active node
                nodes.nodes[n]["type"] = "active"
            else:
                nodes.nodes[n]["type"] = "passive"



    def draw_circuit(self, **kwargs):
        def color_map(graph):
            for i in self.components:
                if type(i) is Inductor:
                    yield "green"
                elif type(i) is Capacitor:
                    yield "red"
                else:
                    yield "blue"
        nx.draw_circular(self.graph,
                         labels={i: x.value for i, x in enumerate(self.components)},
                         node_color=list(color_map(self.graph)),
                         **kwargs)

    @classmethod
    def random_circuit(cls, n, num_extra_edges=None):
        component_types = [c for c in random.choices([Capacitor, Inductor], k=n)]
        components = []
        for c in component_types:
            if c is Capacitor:
                components.append(c(random.randint(0, 10)))
            elif c is Inductor:
                components.append(c(random.randint(0, 10), random.randint(0, 10)))
        graph = nx.cycle_graph(n)
        max_edges = n * (n - 1) // 2
        num_extra_edges = num_extra_edges or random.randint(0, max_edges)
        extra_edges = []
        while len(extra_edges) < num_extra_edges:
            edge = (random.randint(0, n - 1), random.randint(0, n - 1))
            if edge[0] == edge[1]:
                continue
            if edge in extra_edges:
                continue
            if edge[::-1] in extra_edges:
                continue
            extra_edges.append(edge)
        graph.add_edges_from(extra_edges)
        return cls(graph, components)


if __name__ == "__main__":
    circuit = Circuit.random_circuit(10)
    circuit.draw_circuit()
    plt.show()
