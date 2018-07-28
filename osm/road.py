# --------------------------------------------------------------------
# The osmRoad is
#
# Copyright (c) 2018 by Zhongpu Chen (chenloveit@gmail.com)
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------
from scipy.sparse import lil_matrix
import numpy as np
import networkx as nx


def extract_connectivity(parsed_osm):
    nodes = parsed_osm['nodes']
    ways = parsed_osm['ways']

    matrix = lil_matrix((len(nodes), len(nodes)), dtype=np.int64)
    for way in ways:
        nodes_in_way = way[0]
        for i in range(0, len(nodes_in_way) - 1):
            if nodes_in_way[i] == nodes_in_way[i + 1]:
                continue  # remove self loop
            if nodes_in_way[i] not in nodes or nodes_in_way[i + 1] not in nodes:
                continue
            start_idx = nodes[nodes_in_way[i]]
            end_idx = nodes[nodes_in_way[i + 1]]
            # note that for simplicity, oneway is ignored
            # refer to https://wiki.openstreetmap.org/wiki/Key:oneway
            matrix[start_idx, end_idx] = 1
            matrix[end_idx, start_idx] = 1
    return matrix


def extract_adj(parsed_osm):
    nodes = parsed_osm['nodes']
    ways = parsed_osm['ways']
    adj = {}
    for way in ways:
        nodes_in_way = way[0]
        for i in range(0, len(nodes_in_way) - 1):
            if nodes_in_way[i] == nodes_in_way[i + 1]:
                continue  # remove self loop
            if nodes_in_way[i] not in nodes or nodes_in_way[i + 1] not in nodes:
                continue
            if nodes_in_way[i] in adj:
                adj[nodes_in_way[i]].add(nodes_in_way[i + 1])
            else:
                adj[nodes_in_way[i]] = {nodes_in_way[i + 1]}
            if nodes_in_way[i + 1] in adj:
                adj[nodes_in_way[i + 1]].add(nodes_in_way[i])
            else:
                adj[nodes_in_way[i + 1]] = {nodes_in_way[i]}
    return adj


def extract_edges(parsed_osm):
    nodes = parsed_osm['nodes']
    ways = parsed_osm['ways']
    edges = []
    for way in ways:
        nodes_in_way = way[0]
        for i in range(0, len(nodes_in_way) - 1):
            if nodes_in_way[i] == nodes_in_way[i + 1]:
                continue  # remove self loop
            if nodes_in_way[i] not in nodes or nodes_in_way[i + 1] not in nodes:
                continue
            edges.append((nodes_in_way[i], nodes_in_way[i + 1]))
    return edges


def build_graph(parsed_osmxy):
    edges = extract_edges(parsed_osmxy)
    nodes = parsed_osmxy['nodes']

    def dist(x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1],  weight=dist(nodes[edge[0]][0], nodes[edge[0]][1],
                                                  nodes[edge[1]][0], nodes[edge[1]][1]))
    return G

