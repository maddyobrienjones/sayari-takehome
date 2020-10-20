import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.drawing.nx_pydot import graphviz_layout
from networkx.generators.atlas import graph_atlas_g
import random

df = pd.read_csv("request_data.csv")
df = df[["NAME", "Registered Agent", "Commercial Registered Agent", "Owners", "Unnamed: 21"]]
loop_columns = ["Registered Agent", "Commercial Registered Agent", "Owners", "Unnamed: 21"]

# convert dataframe of business information to list of edges between
# businesses and registered agents/owners
graph_df = df.set_index("NAME").stack(dropna=True).reset_index()
graph_df = graph_df[["NAME", 0]]
graph_df.columns = ["Business", "Owner/Agent"]
graph = nx.from_pandas_edgelist(graph_df, "Business", "Owner/Agent")

# setting up plot to label nodes if degree is greater than 1
# to detect whether there are any agents tied to many companies
# or companies tied to many agents
# will be easy to tell company or agent because all companies start with X
labels = {}
for node in graph.nodes():
    if graph.degree[node] > 1:
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
