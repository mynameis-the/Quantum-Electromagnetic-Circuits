# The General Idea
implement the method of nodes for symbolically solving for flux (? i don't know what it is) described in [this paper](https://arxiv.org/abs/1610.03438v2) (2.1.7).
## Instructions In Caveman Language
1. Cavman brain defines circuit components.
2. Oooga booga assemble a circuit by putting components into a graph.
3. bash graph with rock to convert graph of components to graph of nodes, where
active nodes are where inductances and capacitances meet, and passive nodes are
where only capacitances or only inductances meet.
4. caveman enumerates graph nodes, where active nodes are 
$1\ldots N$ and passive nodes are $N+1\ldots P$.
5. Construct the (symmetric) $P\times P$ inverse inductance matrix $\left\lbrack L^{-1}\right\rbrack_{jk}$
who's non-diagonal matrix elements are $-1\/L_{jk}$, where $L_{jk}$ is the value of
the inductance connecting the nodes $j$ and $k$ ($-1\/L_{jk}=0$ if there is none), and who's
diagonal elements are the opposite of the sum of values in the corresponding row or column.
6. Construct the (symmetric) $P\times P$ capacitance matrix $\left\lbrack C\right\rbrack_{rs}$
who's non-diagonal matrix elements are $-C_{rs}$ where $C_{rs}$ is the value of
the capacitance connecting the nodes $r$ and $s$, and who's diagonal elements are
built in the same way as those of $\left\lbrack L^{-1}\right\rbrack_{jk}$.
7. caveman use networkx api to generate spanning tree of capacitance sub-network
in respect to some arbitrary "ground" node (should be specified by input circuit caveman).
8. ooga booga program Hamiltonian formula:

$$\mathcal{H}=\varepsilon_{\text{kin}}+\varepsilon_{\text{pot}}$$

$$\varepsilon_{\text{kin}}=\frac12\vec{\dot{\phi}}^{t}\left\lbrack C\right\rbrack\vec{\dot{\phi}}$$

$$\varepsilon_{\text{pot}}=\frac12\vec{\phi^t}\left\lbrack L^{-1}\right\rbrack\vec{\phi}+\sum_{b}\frac{1}{L_{b}}\left(\phi_{n}-\phi_{n^{\prime}}\right)\tilde{\phi_b}$$

9. Caveman brain plugs Hamilton's equations into sympy solver

# disclaimer
This program solves an electrical circuit for its flux. 

Don't use this. I don't know what a circuit is. I don't know what flux is, and i don't know what electricity is.

I made this while mildly delirious from two vaccines in opposite arms, and it serves no purpose. There is probably going to be something wrong with it.

It also can't solve big systems of differential equations (from circuits around n>5) symbolically because of sympy limitations.
