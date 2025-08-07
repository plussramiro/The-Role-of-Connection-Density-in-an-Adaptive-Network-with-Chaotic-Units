import numpy as np
from numba import njit


@njit
def f(x, a):
    """
    Logistic map: 1.0 - a * x^2
    Works on scalars and arrays with automatic parallelization.

    Args:
        x (float or ndarray): Input value(s).
        a (float): Map parameter controlling the system's behavior.

    Returns:
        float or ndarray: Evaluated logistic map value(s).
    """

    return 1.0 - a * x**2

@njit
def vector(M0, X0, M, epsilon, a):
    """
    Computes the state Z based on the current states X0, adjacency matrix M0, and parameters.

    Args:
        M0 (ndarray): Adjacency matrix.
        X0 (ndarray): Current states of the nodes.
        M (ndarray): Node degrees.
        N (int): Number of nodes.
        epsilon (float): Coupling parameter.
        a (float): Parameter of the dynamical system.

    Returns:
        ndarray: Updated Z vector.
    """

    F = f(X0, a)
    Z = np.dot(M0, F) # Compute the matrix product M0 @ F
    Z = np.where(M > 0, (epsilon / M) * Z, 0) # Ajustar los valores de Z donde M[i] == 0

    return Z

@njit
def update_adjacency_matrix(M0, Y, M, N, X0):
    """
    Updates the adjacency matrix (M0) and associated structures
    based on minimum and maximum distances between nodes.

    Removes disconnected nodes without attempting to reconnect them.

    Args:
        M0 (numpy.ndarray): Adjacency matrix.
        Y (numpy.ndarray): Vector of current node states.
        M (numpy.ndarray): Vector of node degrees.
        N (int): Number of nodes.
        X0 (numpy.ndarray): Vector of initial node states.

    Returns:
        tuple: Updated (M0, Y, M, N, X0).
    """

    i = np.random.randint(0, N) # Select a random node
    DIST = np.abs(Y - Y[i]) # Compute distances from node i to all other nodes
    DIST[i] = np.inf  # Avoid selecting the same node
    vecinos = np.where(M0[i] == 1)[0] # Identify neighbors of node i and compute their distances
    
    if vecinos.size > 0:
        DIST_MAX = DIST[vecinos]  # Only distances of connected nodes
        index_list_max = vecinos[np.argmax(DIST_MAX)]  # Index of the farthest node

    # Find the minimum distance
    if np.any(DIST < np.inf):  # Check that there are other nodes available
        index_list_min = np.argmin(DIST)
    else:
        return M0, Y, M, N, X0  # If no other nodes are available, return

    # If there are neighbors and the node with minimum distance is not a neighbor, perform the swap
    if vecinos.size > 0 and M0[i, index_list_min] == 0:
        M0[i, index_list_min] = 1
        M0[index_list_min, i] = 1
        M0[i, index_list_max] = 0
        M0[index_list_max, i] = 0

        # Update node degrees
        M[i] = np.sum(M0[i])
        M[index_list_min] = np.sum(M0[index_list_min])
        M[index_list_max] = np.sum(M0[index_list_max])

    # Remove nodes that have no remaining connections
    isolated_nodes = np.where(M == 0)[0]
    if isolated_nodes.size > 0:
        mask = np.ones(N, dtype=np.bool_)
        mask[isolated_nodes] = False
        M0 = M0[mask][:, mask]  # Filter matrix by removing isolated nodes
        Y = Y[mask]
        M = M[mask]
        X0 = X0[mask]
        N = M.size  # New number of nodes
    return M0, Y, M, N, X0