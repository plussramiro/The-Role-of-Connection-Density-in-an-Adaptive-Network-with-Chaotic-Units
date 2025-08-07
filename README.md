# The Role of Connection Density in an Adaptive Network with Chaotic Units

This repository contains the source code, simulation data, and analysis tools for the study:

**“The Role of Connection Density in an Adaptive Network with Chaotic Units”**

In this work, we investigate how the average degree of connectivity, considered as a density parameter, shapes the global dynamics and structural properties of adaptive networks composed of chaotic units. Building upon the model introduced by Gong and van Leeuwen [(EPL, 2004)](https://iopscience.iop.org/article/10.1209/epl/i2003-10287-7), originally motivated by cortical self-organization, we explore how network topology evolves through adaptive rewiring. Our results highlight changes in small-worldness, clustering, and modular organization — phenomena relevant to neural systems.


---

## 📁 Repository Structure

```
├── src/                      # Source code modules
│   ├── functions.py          # Network metric computation functions
│   ├── model.py              # Kaneko adaptive network model implementation
│   └── utils.py              # Utility functions
│
├── results/                  # Processed network metrics and outputs
│   └── results_p*/           # Organized by rewiring probability p
│       └── simulation_*/     # Multiple repetitions
│           └── networks/     # Matrices used for metric analysis
│
├── figures/                  # Generated plots for the paper
├── analysis.ipynb           # Jupyter Notebook for analyzing results
├── main.py                  # Entry point for simulations
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🧪 How to Run the Simulations

### 1. Clone the repository
```bash
git clone https://github.com/ramirop2021/The-Role-of-Connection-Density-in-an-Adaptive-Network-with-Chaotic-Units.git
cd The-Role-of-Connection-Density-in-an-Adaptive-Network-with-Chaotic-Units
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate.bat     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the main simulation script
```bash
python main.py
```

> Simulations are automatically saved under `results/` with organized folder structure.

---

## 📊 Analysis

- Run `analysis.ipynb` to generate the main figures and metrics reported in the paper.
- Network properties such as clustering coefficient, average shortest path, small-world index, and Louvain cluster structure are computed from pre-simulated matrices stored in `results/`.

---

## 🔧 Dependencies

- numpy
- pandas
- networkx
- matplotlib
- community (python-louvain)
- tqdm

All dependencies are listed in `requirements.txt`.

---

## 📬 Contact

If you have questions or want to contribute, feel free to reach out:

**Ramiro Plüss**  
[Email](mailto:rpluss@itba.edu.ar)  

[LinkedIn Profile](https://www.linkedin.com/in/ramiropluss/)

[GitHub Profile](https://github.com/ramirop2021)  

---

## 📄 Citation

The accompanying research paper is available as a preprint on arXiv:  
https://arxiv.org/abs/2505.11437


