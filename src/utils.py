import os
import numpy as np
import json
import networkx as nx

def analyze_and_save_metrics(M0, STATES, epsilon_k, step, save_matrix, save_states, simulation_dir, N):


    """
    Analyzes network metrics and saves the results to the corresponding files.

    Args:
        M0 (numpy.ndarray): Adjacency matrix.
        STATES (numpy.ndarray): Node states.
        epsilon_k (float): Current epsilon value.
        step (int): Current number of time steps.
        SAVE_MATRIX (bool): Whether to save the adjacency matrix.
        SAVE_STATES (bool): Whether to save node states.
        simulation_dir (str): Base path for the specific simulation.
        N (int): Size of the current network.
    """


    # Create graph from the adjacency matrix
    G = nx.from_numpy_array(M0)

    # ------------------------- SAVE MATRICES --------------------------
    if save_matrix:
        matrix_dir = os.path.join(simulation_dir, "networks", f"eps_{epsilon_k:.3f}")
        os.makedirs(matrix_dir, exist_ok=True)
        np.savetxt(
            os.path.join(matrix_dir, f"matrix_eps_{epsilon_k:.3f}_step_{step}.txt"),
            M0,
            fmt="%i",
            delimiter=",",
        )
    # ---------------------------------------------------------------------

    # -------------------------- SAVE STATES --------------------------
    if save_states:
        states_dir = os.path.join(simulation_dir, "states", f"eps_{epsilon_k:.3f}")
        os.makedirs(states_dir, exist_ok=True)
        np.savetxt(
            os.path.join(states_dir, f"states_eps_{epsilon_k:.3f}_step_{step}.txt"),
            STATES,
            delimiter=",",
        )
    # ---------------------------------------------------------------------

def create_folders(epsilon, save_matrix, save_states, N, num_simulations, results_dir="results"):
    """
    Creates the required folders for saving simulation outputs,
    according to the selected options.

    Args:
        epsilon (list or numpy.ndarray): List or array of epsilon values.
        save_matrix (bool): Whether to create folders for adjacency matrices.
        save_states (bool): Whether to create folders for node state snapshots.
        N (int): Number of nodes in the network.
        num_simulations (int): Number of simulations to run for the given N.
        results_dir (str): Root directory where results will be saved.
    """
    base_dir = results_dir
    os.makedirs(base_dir, exist_ok=True)

    for sim in range(num_simulations):
        sim_dir = os.path.join(base_dir, f'simulation_{sim + 1}')

        if save_matrix:
            for eps in epsilon:
                matrix_dir = os.path.join(sim_dir, f'networks/eps_{eps:.3f}')
                os.makedirs(matrix_dir, exist_ok=True)

        if save_states:
            for eps in epsilon:
                states_dir = os.path.join(sim_dir, f'states/eps_{eps:.3f}')
                os.makedirs(states_dir, exist_ok=True)

def read_json(filepath):
    """
    Reads a JSON configuration file and returns its contents as a dictionary.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict: Parsed configuration parameters.
    """
    with open(filepath, "r") as f:
        return json.load(f)

def print_header(word):
    L = 60 - len(word)
    print(L//2*"/" + word + L//2*"/")