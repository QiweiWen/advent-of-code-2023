import networkx as nx
import sys
from pyvis.network import Network
import pandas as pd
from collections import defaultdict


def parse_input(inf):
    edges = defaultdict(list)

    for line in inf:
        connect_from, connect_to = [x.strip() for x in line.split("->")]
        connect_to = [x.strip() for x in connect_to.split(",")]

        node_name = connect_from
        if connect_from[0] == "%":
            node_name = connect_from[1:]
        elif connect_from[0] == "&":
            node_name = connect_from[1:]

        edges[node_name] += connect_to

    graph = {"Source": [], "Target": []}
    for node_from, node_tos in edges.items():
        for node_to in node_tos:
            graph["Source"].append(node_from)
            graph["Target"].append(node_to)
            graph["Type"] = "Directed"

    graph = pd.DataFrame(graph)
    return graph


if __name__ == "__main__":
    inf = sys.argv[1]
    with open(inf, "r") as inf:
        graph = parse_input(inf)
    graph = nx.from_pandas_edgelist(
        graph, source="Source", target="Target", create_using=nx.DiGraph)

    net = Network(notebook=True, directed=True, cdn_resources="remote")
    net.from_nx(graph)
    net.show("example.html")
