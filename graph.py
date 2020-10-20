import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.generators.atlas import graph_atlas_g
import random
import numpy as np

# importing data and getting rid of extraneous columns
df = pd.read_csv("request_data.csv")
df = df[["NAME", "Registered Agent", "Commercial Registered Agent", "Owners", "Unnamed: 21"]]
loop_columns = df.columns[1:]

# convert dataframe of business information to list of edges between
# businesses and registered agents/owners
graph_df = df.set_index("NAME").stack(dropna=True).reset_index()
graph_df = graph_df[["NAME", 0]]
graph_df.columns = ["source", "target"]
graph = nx.from_pandas_edgelist(graph_df, "source", "target")

# add edges between agents and owners
for i in range(len(loop_columns)-1):
    graph.add_edges_from(zip(df[loop_columns[i]], df[loop_columns[i+1]]))

# to get rid of edges between a node and nothing added by the above loop
graph.remove_node(np.nan)

# setting up plot to label nodes if degree is greater than 2
# to detect whether there are any agents tied to many companies
# using degree of 3 as minimum because some companies have both an owner and
# registered agent, and will make the graph cluttered
labels = {}
for node in graph.nodes():
    if graph.degree[node] > 2:
        # to get rid of addresses in agent information
        labels[node] = node.split("\n")[0]

# rendering plot
plt.figure(1, figsize=(8, 8))
# making layout more aesthetically pleasing
pos = graphviz_layout(graph, prog="neato")
# setting up list of subgraphs to provide color differentation between
# them
C = (graph.subgraph(c) for c in nx.connected_components(graph))
for g in C:
    c = [random.random()] * nx.number_of_nodes(g)  # random color
    nx.draw(g, pos, node_size=40, node_color=c, vmin=0.0, vmax=1.0, with_labels=False)
    nx.draw_networkx_labels(g, pos, labels, font_size=10)

plt.savefig("business_owneragent_plot.png", format="PNG")
