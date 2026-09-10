import os
import time
import numpy as np

from src.utils import read_json, print_header, create_folders, analyze_and_save_metrics
from src.model import f, vector, update_adjacency_matrix
from src.functions import compute_network_metrics, compute_louvain_cluster_metrics


def main():
    # Load configuration
    path_json = "config.json"
    parameters = read_json(path_json)

    # Parameters
    N_init = parameters["N"]
    T = parameters["T"]
    a = parameters["a"]
    time_steps = parameters["time_steps"]
    epsilon = parameters["epsilon"]
    p = parameters["p"]
    num_simulations = parameters["num_simulations"]
    save_matrix = parameters["options"]["save_matrix"]
    save_states = parameters["options"]["save_states"]

    # Define results directory
    results_dir = f"results_p{p:.3f}"

    # Print configuration
    print_header(" PARAMETERS ")
    print(f"T = {T}, N = {N_init}, a = {a}, epsilon = {epsilon}, p = {p}")
    print(f"num_simulations = {num_simulations}")
    print(f"time_steps = {time_steps}")
    print_header(" SAVING OPTIONS ")
    print(f"save_matrix = {save_matrix}")
    print(f"save_states = {save_states}")
    print_header("")
    print("\n")

    # Prepare folders
    create_folders(epsilon, save_matrix, save_states, N_init, num_simulations, results_dir=results_dir)

    # Run simulations
    sim_real = 1
    out_file = os.path.join(results_dir, "network_metrics.txt")
    with open(out_file, "w") as outfile:
        header = "epsilon,simulation,time_step,clustering,path_length,omega,s1,s2,<s>,<s>_std,n_s,N\n"
        outfile.write(header)

        print("Metrics log\n")
        for sim in range(num_simulations):
            simulation_dir = os.path.join(results_dir, f"simulation_{sim + sim_real}")
            os.makedirs(simulation_dir, exist_ok=True)

            for k, eps in enumerate(epsilon):
                # IMPORTANT: each epsilon condition starts from the same initial node count
                # (do not inherit reduced N from a previous epsilon run).
                N = N_init
                M0 = (np.random.rand(N, N) < p).astype(np.float64)
                M0 = np.triu(M0, 1)
                M0 += M0.T
                M = np.sum(M0, axis=1)
                X0 = np.random.uniform(low=-1.0, high=1.0, size=N)
                snapshot_rng = np.random.default_rng()

                def save_snapshot(step, adjacency, states, node_count):
                    """Save a topology and states evaluated for that same topology."""
                    C, L, omega = compute_network_metrics(adjacency)
                    s1, s2, s_mean, s_std, n_s = compute_louvain_cluster_metrics(adjacency)

                    print(f"epsilon: {eps:.3f}, step: {step}, clustering: {C:.4f}, path length: {L:.4f}, "
                          f"omega: {omega:.4f}, s1: {s1}, s2: {s2}, <s>: {s_mean:.2f}, std: {s_std:.2f}, "
                          f"n_s: {n_s}, simulation: {sim + sim_real}, N = {node_count}")

                    outfile.write(f"{eps},{sim + sim_real},{step},{C},{L},{omega},"
                                  f"{s1},{s2},{s_mean},{s_std},{n_s},{node_count}\n")

                    analyze_and_save_metrics(adjacency, states, eps, step,
                                             save_matrix, save_states, simulation_dir, node_count)

                # step_0 is the untouched initial pair (M(0), x(0)): no dynamics and no rewiring.
                save_snapshot(0, M0, X0, N)

                for step in range(1, time_steps + 1):
                    # Preserve the original protocol: node states are initialized anew
                    # for every adaptive cycle (the first cycle uses the saved x(0)).
                    if step > 1:
                        X0 = np.random.uniform(low=-1.0, high=1.0, size=N)

                    for _ in range(T):
                        X0 = (1.0 - eps) * f(X0, a) + vector(M0, X0, M, eps, a)

                    # Complete adaptive step t and obtain M(t).
                    M0, _, M, N, X0 = update_adjacency_matrix(M0, X0, M, N, X0)

                    if step % 1000 == 0:
                        # Evaluate the archived state directly on M(t). This keeps
                        # matrix_step_t and states_step_t synchronized.
                        snapshot_states = snapshot_rng.uniform(low=-1.0, high=1.0, size=N)
                        for _ in range(T):
                            snapshot_states = ((1.0 - eps) * f(snapshot_states, a)
                                               + vector(M0, snapshot_states, M, eps, a))

                        save_snapshot(step, M0, snapshot_states, N)

        print("Done.")

if __name__ == "__main__":
    main()
