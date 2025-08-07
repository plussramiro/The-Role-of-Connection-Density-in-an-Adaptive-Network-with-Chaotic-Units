from numba import njit
import numpy as np
import networkx as nx
import community  # python-louvain
import pandas as pd

def get_largest_connected_component(adj_matrix):
    G = nx.from_numpy_array(adj_matrix)
    if nx.is_connected(G):
        return adj_matrix
    else:
        largest_cc = max(nx.connected_components(G), key=len)
        idx = sorted(list(largest_cc))
        return adj_matrix[np.ix_(idx, idx)]

def compute_network_metrics(adj_matrix):
    """
    Computes average clustering (C), average shortest path length (L),
    and the small-world index (omega) using the ratio-based definition:
    omega = (C / Crand) / (L / Lrand)

    Returns:
        tuple: (C, L, omega) or (np.nan, np.nan, np.nan) if not computable.
    """
    G_lcc = get_largest_connected_component(adj_matrix)
    if G_lcc is None or G_lcc.shape[0] < 2:
        return np.nan, np.nan, np.nan

    G = nx.from_numpy_array(G_lcc)
    C = nx.average_clustering(G)

    try:
        L = nx.average_shortest_path_length(G)
    except nx.NetworkXError:
        return np.nan, np.nan, np.nan

    N = G.number_of_nodes()
    E = G.number_of_edges()
    if E == 0:
        return np.nan, np.nan, np.nan

    # Generate a connected random graph with same N and E
    for _ in range(5):
        rand_G = nx.gnm_random_graph(N, E)
        if nx.is_connected(rand_G):
            break
    else:
        return np.nan, np.nan, np.nan

    Crand = nx.average_clustering(rand_G)
    Lrand = nx.average_shortest_path_length(rand_G)

    if L == 0 or Crand == 0 or Lrand == 0:
        return np.nan, np.nan, np.nan

    omega = (C / Crand) / (L / Lrand)
    return C, L, omega

def compute_louvain_cluster_metrics(adj_matrix):
    """
    Calcula métricas de los grupos detectados por Louvain en una red.

    Args:
        adj_matrix (numpy.ndarray): Matriz de adyacencia.

    Returns:
        tuple: (s1, s2, mean_cluster, std_cluster, num_clusters)
    """
    try:
        G = nx.from_numpy_array(adj_matrix)
        #print("Louvain N:", G.number_of_nodes(), "E:", G.number_of_edges())
        if G.number_of_edges() == 0:
            return 0, 0, 0, 0, 0

        partition = community.best_partition(G)
        cluster_sizes = np.array(list(pd.Series(partition).value_counts()))

        s1 = cluster_sizes[0] if len(cluster_sizes) > 0 else 0
        s2 = cluster_sizes[1] if len(cluster_sizes) > 1 else 0
        mean_cluster = np.mean(cluster_sizes) if len(cluster_sizes) > 0 else 0
        std_cluster = np.std(cluster_sizes) if len(cluster_sizes) > 0 else 0
        num_clusters = len(cluster_sizes)
        return s1, s2, mean_cluster, std_cluster, num_clusters
    except Exception as e:
        print(f"Error en Louvain: {e}")
        return 0, 0, 0, 0, 0