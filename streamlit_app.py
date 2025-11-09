# streamlit_app.py
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq, time

# === Graph Definition ===
graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'A': 4, 'C': 1, 'D': 5},
    'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
    'D': {'B': 5, 'C': 8, 'E': 2, 'Z': 6},
    'E': {'C': 10, 'D': 2, 'Z': 3},
    'Z': {'D': 6, 'E': 3}
}

# === Prim’s Algorithm ===
def prim_mst(start):
    visited = set([start])
    edges = []
    mst_edges = []

    for to, w in graph[start].items():
        heapq.heappush(edges, (w, start, to))

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst_edges.append((frm, to, weight))
            for next_to, next_w in graph[to].items():
                if next_to not in visited:
                    heapq.heappush(edges, (next_w, to, next_to))
    return mst_edges

# === Draw Graph ===
def draw_graph(highlight_edges=[]):
    G = nx.Graph()
    for u in graph:
        for v, w in graph[u].items():
            G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(6,4))
    nx.draw(G, pos, with_labels=True, node_color="#BBDEFB", edge_color='gray', node_size=900, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    if highlight_edges:
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='green', width=3)
    st.pyplot(plt)

# === Web UI ===
st.title("🚁 Drone MST Mission Control (Web)")

username = st.text_input("Pilot Name ✈️")
start_node = st.selectbox("Start Node", list(graph.keys()))
speed = st.slider("Drone Speed", 0.5, 3.0, 1.5)
launch = st.button("🚀 Launch Drone")

if launch:
    if not username:
        st.warning("Please enter your name to start the mission!")
    else:
        mst = prim_mst(start_node)
        st.success(f"MST Created with {len(mst)} edges. Total Cost = {sum(w for _,_,w in mst)} units.")
        progress = st.progress(0)
        highlight = []
        total_edges = len(mst)
        for i, (u, v, w) in enumerate(mst, 1):
            highlight.append((u, v))
            st.info(f"🚁 Drone moving from {u} → {v} | Cost {w}")
            draw_graph(highlight)
            progress.progress(i / total_edges)
            time.sleep(3.5 - speed)
        st.success("🎉 Mission Complete! Drone visited all nodes successfully.")
