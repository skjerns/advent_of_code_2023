#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 13:49:19 2023

@author: simon
"""
import networkx
from itertools import combinations, product
from tqdm import tqdm
test_input = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""


c = test_input

with open('day25_input.txt', 'r') as f:
    c = f.read().strip()

graph = networkx.Graph()

for row in c.split('\n'):
    node1, *other_nodes = row.replace(':', '').split(' ')
    for node2 in other_nodes:
        graph.add_edge(node1, node2)




# stop
#%% first attempt via betweeness centrality of nodes

#  this takes too long :( no chance

nodes_centrality = sorted(networkx.betweenness_centrality(graph).items(),
                          key=lambda x:x[1], reverse=True)
important_nodes = [x[0] for x in nodes_centrality[:25]]
possible_removals = list(combinations(important_nodes, 3))
for nodes in tqdm(possible_removals):
    for other_nodes in product(*[list(graph[node]) for node in nodes]):
        remove_edges = list(zip(nodes, other_nodes))
        graph_removed = graph.copy()
        graph_removed.remove_edges_from(remove_edges)
        # assert len(graph_removed.edges)==len(graph.edges)-3
        subgraphs = list(networkx.connected_components(graph_removed))
        # print(len(to_remove))
        if len(subgraphs)==2:
            break

print(len(subgraphs[0])*len(subgraphs[1]))


#%% convert to linegraph first! centrality on edges :)

linegraph = networkx.line_graph(graph)

nodes_centrality = sorted(networkx.betweenness_centrality(linegraph).items(),
                          key=lambda x:x[1], reverse=True)

important_edges = [x[0] for x in nodes_centrality[:25]]


possible_removals = list(combinations(important_edges, 3))
for remove_edges in tqdm(possible_removals):
    graph_removed = graph.copy()
    graph_removed.remove_edges_from(remove_edges)
    # assert len(graph_removed.edges)==len(graph.edges)-3
    subgraphs = list(networkx.connected_components(graph_removed))
    # print(len(to_remove))
    if len(subgraphs)==2:
            break

print(len(subgraphs[0])*len(subgraphs[1]))
