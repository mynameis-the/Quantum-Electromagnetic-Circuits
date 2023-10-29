from typing import Optional, List

import random
import numpy as np
import networkx as nx
from dataclasses import dataclass, field
import sympy
from sympy import *
from sympy.physics.mechanics import *
from sympy.abc import t
import matplotlib.pyplot as plt

from components import Component, Capacitor, Inductor


@dataclass
class Circuit:
    graph: nx.Graph
    components: Optional[List[Component]] = None

    def solve(self, offset_flux: List[List[float]]=None):  # caveman logic
        # graph of nodes
        nodes = nx.line_graph(self.graph)
        # determine active nodes and passive nodes
        for n in nodes.nodes:
            i = self.components[n[0]]
            j = self.components[n[1]]
            # amazing code, always do this
            if i.capacitance != 0 and j.inductance !=0 or j.capacitance != 0 and i.inductance !=0:
                # active node
                nodes.nodes[n]["type"] = "active"
            else:
                # passive node
                nodes.nodes[n]["type"] = "passive"
        p = len(nodes.nodes)

        # construct L^-1
        L_inverse = np.zeros((p, p))
        for n in nodes.nodes:
            j, k = n
            L_jk = self.components[j].inductance + self.components[j].inductance
            if np.isclose(L_jk, 0):
                L_inverse[j][k] = 0
            else:
                L_inverse[j][k] = -1/L_jk
        """
        for i in range(p):
            # idc
            L_inverse[i][i] = np.sum(L_inverse, axis=0)[i]
        """
        diagonal_values = np.sum(L_inverse, axis=0)
        for i in range(p):
            # idc
            #L_inverse[i][i] = np.sum(L_inverse, axis=0)[i]

            # i cared
            L_inverse[i][i] = diagonal_values[i]
        # surprise tool for later
        #L= np.linalg.inv(L_inverse)

        # construct C
        C = np.zeros((p, p))
        for n in nodes:
            r, s = n
            C_rs = self.components[r].capacitance - self.components[s].capacitance
            C[r][s] = -C_rs
        diagonal_values = np.sum(C, axis=0)
        for i in range(p):
            C[i][i] = diagonal_values[i]
        # take ground node to be the 0th element
        ground = 0
        # eliminate ground rows and columns from matrices
        L_inverse = np.delete(L_inverse, ground, axis=0)
        L_inverse = np.delete(L_inverse, ground, axis=1)
        C = np.delete(C, ground, axis=0)
        C = np.delete(C, ground, axis=1)
        # initialise hamiltonian variables
        phi = sympy.Matrix([sympy.Function(f"phi_{i}")(t) for i in range(p-1)])
        phi_dot = phi.diff(t)
        offset_flux = offset_flux or np.zeros((p, p))
        # (no idea what this bit does and the paper doesn't explain it)
        josephson_doohickey = 0
        for i, b in enumerate(nodes):
            if nodes.nodes[b]["type"] == "passive":
                j, k = b
                #L_b =  L[j][k]
                phi_squiggle_b = offset_flux[j][k]
                #josephson_doohickey += 1/L_b*(phi[j]-phi[k])*phi_squiggle_b
        # caveman brain write out formulae
        e_potential = (sympy.Rational(1, 2)*phi.T*L_inverse*phi)[0]+josephson_doohickey
        e_kinetic = (sympy.Rational(1, 2)*phi_dot.T*C*phi_dot)[0]
        LE = e_kinetic - e_potential
        # solve lagrangian
        LM = LagrangesMethod(LE, phi)
        eq_matrix = LM.form_lagranges_equations()
        if 0 in eq_matrix:
            return eq_matrix
        return dsolve(eq_matrix)

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
        num_extra_edges = num_extra_edges if num_extra_edges is not None else random.randint(0, max_edges)
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
    sympy.init_printing()
    circuit = Circuit.random_circuit(3, num_extra_edges=0)
    motion = circuit.solve()
    for eq in motion:
        print(eq)
    circuit.draw_circuit()
    plt.show()
