import copy
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random
import matplotlib as mpl

# Credit to this stackoverflow thread for the hierarchical layout:
# https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3/29597209#29597209
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

class Graph:
    next_id = 1
    maxi = float('-inf')
    mini = np.inf

    @staticmethod
    def add_children(node, G: nx.DiGraph, id_node: int, labels):
        for i in range(len(node.children)):
            child = node.children[i]
            current_id = copy.copy(Graph.next_id)
            value = child.value / max([1, child.visit])
            G.add_node("Child_%i" % Graph.next_id, weight=child.data.player)
            G.add_edge("Child_%i" % id_node, "Child_%i" % current_id, weight=value)
            Graph.next_id += 1
            if value < Graph.mini:
                Graph.mini = value
            if value > Graph.maxi:
                Graph.maxi = value
            labels[f'Child_{current_id}'] = child.data.game.toString_graph()
            if len(child.children) > 0:
                Graph.add_children(child, G, current_id, labels)

    @staticmethod
    def build_graph(root, iter):
        fig, ax = plt.subplots(figsize=(12, 12))
        fig.set_facecolor('black')
        plt.axis('off')
        G = nx.DiGraph()
        labels = {}


        G.add_node("Child_0", weight=root.data.player)
        labels["Child_0"] = root.data.game.toString_graph()
        Graph.add_children(root, G, 0, labels)

        plt.title('draw_networkx')
        pos = hierarchy_pos(G, width=1., vert_gap = 0.2)
        nodes = nx.draw_networkx_nodes(G, pos, node_size=1000, cmap=plt.cm.bwr,
                                       node_color=[G.nodes[u]['weight']
                                                      for u in G.nodes], vmin=1, vmax=2)
        nodes.set_edgecolor(c="white")

        edges = nx.draw_networkx_edges(G, pos, arrowsize=1, node_size=1000,
                                       edge_cmap= plt.cm.summer, width=1, edge_color=[G[u][v]['weight']
                                                      for u, v in G.edges], edge_vmax=Graph.maxi, edge_vmin=Graph.mini)

        nx.draw_networkx_labels(G, pos, labels=labels, font_size=6)
        pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.summer)
        pc.set_array(range(2))
        cbar = plt.colorbar(pc, ax=ax,location='bottom')
        cbar.outline.set_edgecolor('white')
        cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
        cbar.set_label('Average edge value', color='white')
        plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white')

        markers = ["o"]
        f = lambda m, c: plt.plot([], [], marker=m, color=c, ls="none")[0]
        handles = [f(markers[0], "k") for i in range(2)]
        labels = ["Player 1", "Player 2"]
        leg = ax.legend(handles, labels, loc='upper left', framealpha=1, markerscale=2, facecolor="dimgray", labelcolor='white')
        leg.legendHandles[0].set_color('blue')
        leg.legendHandles[1].set_color('red')

        plt.show()
        fig.savefig(f'example{iter}.png', dpi=150)
        plt.close()
        Graph.next_id = 1
        Graph.maxi = float('-inf')
        Graph.mini = np.inf