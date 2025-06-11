import glob
import os

import numpy as np


if __name__ == "__main__":
    folder = "output/stochastic"
    filepattern = "samples-1e3-run-*.txt"
    os.chdir(folder)

    full_data = []
    x_coords = np.empty(0)  # Just need a placeholder

    for file in glob.glob(filepattern):
        x_coords, qrad = np.loadtxt(file, delimiter=",").T
        full_data.append(qrad)

    full_data = np.vstack(full_data)
    qrad_est = np.mean(full_data, axis=0)
    qrad_std = np.std(full_data, axis=0)

    np.savetxt(
        "samples-1e3-agg.txt",
        np.column_stack([x_coords, qrad_est, qrad_std]),
        header="X_CellCenter Qrad_Est Qrad_Std",
        delimiter=",",
        fmt="%.6f",
    )
