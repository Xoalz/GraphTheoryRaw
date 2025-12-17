import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np

# ---------------- SIDEBAR: LANGUAGE OPTION ----------------
language = st.sidebar.selectbox(
    "🌐 Language / Bahasa",
    ("English", "Bahasa Indonesia")
)

# ---------------- TEXT DICTIONARY ----------------
texts = {
    "English": {
        "title": "Graph Visualization with Degree & Adjacency Matrix",
        "vertices": "Input Number of Vertices:",
        "edges": "Input Number of Edges:",
        "button": "Generate Graph",
        "error": "Number of edges exceeds the maximum:",
        "degree_title": "📌 Degree of Each Node",
        "adj_title": "📌 Adjacency Matrix",
        "node": "Node",
        "degree": "Degree",
        "nodes": "Nodes"
    },
    "Bahasa Indonesia": {
        "title": "Visualisasi Graf dengan Derajat & Matriks Ketetanggaan",
        "vertices": "Masukkan Jumlah Simpul:",
        "edges": "Masukkan Jumlah Sisi:",
        "button": "Buat Graf",
        "error": "Jumlah sisi melebihi maksimum:",
        "degree_title": "📌 Derajat Setiap Simpul",
        "adj_title": "📌 Matriks Ketetanggaan",
        "node": "Simpul",
        "degree": "Derajat",
        "nodes": "Simpul"
    }
}

t = texts[language]

# ---------------- MAIN TITLE ----------------
st.title(t["title"])

# ---------------- INPUT ----------------
num_vertices = st.number_input(
    t["vertices"],
    min_value=1,
    value=5
)

num_edges = st.number_input(
    t["edges"],
    min_value=0,
    value=4
)

# ---------------- BUTTON ACTION ----------------
if st.button(t["button"]):
    G = nx.Graph()
    G.add_nodes_from(range(1, num_vertices + 1))

    possible_edges = [
        (i, j)
        for i in range(1, num_vertices + 1)
        for j in range(i + 1, num_vertices + 1)
    ]

    max_edges = len(possible_edges)

    if num_edges > max_edges:
        st.error(f"{t['error']} {max_edges}")
    else:
        selected_edges = random.sample(possible_edges, num_edges)
        G.add_edges_from(selected_edges)

        # ---------------- GRAPH VISUALIZATION ----------------
        fig, ax = plt.subplots()
        nx.draw(
            G,
            with_labels=True,
            node_color="lightblue",
            node_size=800,
            font_size=12
        )
        st.pyplot(fig)

        st.markdown("---")

        # ---------------- DEGREE ----------------
        st.subheader(t["degree_title"])
        degrees = dict(G.degree())

        degree_df = pd.DataFrame({
            t["node"]: list(degrees.keys()),
            t["degree"]: list(degrees.values())
        })

        st.table(degree_df.style.hide(axis="index"))

        st.markdown("---")

        # ---------------- ADJACENCY MATRIX ----------------
        st.subheader(t["adj_title"])

        adj_matrix = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
        adj_matrix = adj_matrix.astype(int)

        df_matrix = pd.DataFrame(
            adj_matrix,
            index=sorted(G.nodes()),
            columns=sorted(G.nodes())
        )

        df_matrix.index.name = t["nodes"]
        df_matrix.columns.name = t["nodes"]

        st.dataframe(df_matrix)

        st.markdown("---")
