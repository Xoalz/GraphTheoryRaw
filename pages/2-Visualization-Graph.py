import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

st.title("Graph Visualization with Degree & Adjacency Matrix")

num_vertices = st.number_input("Input Amount Of Vertices:", min_value=1, value=5)
num_edges = st.number_input("Input Amount of Edges:", min_value=0, value=4)

if st.button("Generate Graph"):
    G = nx.Graph()
    G.add_nodes_from(range(1, num_vertices + 1))

    possible_edges = [
        (i, j)
        for i in range(1, num_vertices + 1)
        for j in range(i + 1, num_vertices + 1)
    ]

    max_edges = len(possible_edges)

    if num_edges > max_edges:
        st.error(f"Jumlah edges melebihi maksimum: {max_edges}")
    else:
        selected_edges = random.sample(possible_edges, num_edges)
        G.add_edges_from(selected_edges)

        # VISUALISASI GRAPH
        fig, ax = plt.subplots()
        nx.draw(G, with_labels=True, node_color='lightblue',
                node_size=800, font_size=12)
        st.pyplot(fig)

        st.markdown("---")

        # DEGREE
        st.subheader("📌 Degree of Each Node")
        degrees = dict(G.degree())

        degree_df = pd.DataFrame({
            "Node": list(degrees.keys()),
            "Degree": list(degrees.values())
        })

        st.table(degree_df.style.hide(axis="index"))

        st.markdown("---")

        # ADJACENCY MATRIX
        st.subheader("📌 Adjacency Matrix")

        adj_matrix = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
        adj_matrix = adj_matrix.astype(int)

        df_matrix = pd.DataFrame(
            adj_matrix,
            index=sorted(G.nodes()),
            columns=sorted(G.nodes())
        )

        df_matrix.index.name = "Nodes"
        df_matrix.columns.name = "Nodes"

        st.dataframe(df_matrix)

        st.markdown("---")
