import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.generators.atlas import graph_atlas_g
import random

df = pd.read_csv("request_data.csv")
df = df[["NAME", "Registered Agent", "Commercial Registered Agent", "Owners", "Unnamed: 21"]]
loop_columns = ["Registered Agent", "Commercial Registered Agent", "Owners", "Unnamed: 21"]
graph_df = df.set_index("NAME").stack(dropna=True).reset_index()
graph_df = graph_df[["NAME", 0]]
graph_df.columns = ["Business", "Owner/Agent"]

graph = nx.from_pandas_edgelist(graph_df, "Business", "Owner/Agent")

print(nx.number_of_nodes(graph))
print(nx.number_of_edges(graph))
print(nx.number_connected_components(graph))

plt.figure(1, figsize=(8, 8))
pos = graphviz_layout(graph, prog="neato")
C = (graph.subgraph(c) for c in nx.connected_components(graph))
for g in C:
    c = [random.random()] * nx.number_of_nodes(g)  # random color...
    nx.draw(g, pos, node_size=40, node_color=c, vmin=0.0, vmax=1.0, with_labels=False)
plt.show()

#plt.savefig("Graph2.png", format="PNG")
