import pyvista as pv
import numpy as np

# Load the PVD file
reader = pv.PVDReader("../more-grid/lmrsim/vtk/fluid.pvd")
# Take the final time-point
reader.set_active_time_point(-1)
multiblock = reader.read()

print(f"Loaded multiblock with {multiblock.n_blocks} blocks")

# Combine all blocks into a single mesh
mesh = multiblock.combine()

# Get the bounding box of the combined mesh
bounds = mesh.bounds  # [xmin, xmax, ymin, ymax, zmin, zmax]
print(f"Combined mesh bounds: {bounds}")
print(f"Available arrays: {mesh.array_names}")

# Calculate the midpoint height (halfway up the bounding box)
y_mid = (bounds[2] + bounds[3]) / 2 + (
    bounds[3] - bounds[2]
) * 0.01  # (ymin + ymax) / 2

# Define the horizontal line at the midpoint height
x_start, x_end = bounds[0], bounds[1]  # xmin, xmax
z_coord = 0

print(f"Searching for cells intersecting line: y = {y_mid:.6f}, z = {z_coord:.6f}")

# Create a line object
n_line_points = 1000  # Use many points to ensure we catch all intersecting cells
start_point = [x_start, y_mid, z_coord]
end_point = [x_end, y_mid, z_coord]
line = pv.Line(start_point, end_point, resolution=n_line_points - 1)

# Find cells that intersect with the line
intersecting_cells = mesh.find_cells_intersecting_line(start_point, end_point)

print(f"Found {len(intersecting_cells)} cells intersecting the line")

# Get cell centers for the intersecting cells
cell_centers = mesh.cell_centers()
intersecting_centers = cell_centers.points[intersecting_cells]

# Sort by x-coordinate to get ordered points along the line
sort_indices = np.argsort(intersecting_centers[:, 0])
intersecting_cells_sorted = intersecting_cells[sort_indices]
x_coords = intersecting_centers[sort_indices, 0]

# Extract the Qrad values from the intersecting cells
if "Qrad" in mesh.array_names:
    # Get Qrad values for the intersecting cells (sorted by x-coordinate)
    qrad_values = mesh["Qrad"][intersecting_cells_sorted]

    print(f"Extracted {len(qrad_values)} Qrad values from intersecting cells")
    print(f"X-coordinate range: {x_coords.min():.6f} to {x_coords.max():.6f}")

    # Print some statistics
    print(f"Qrad range: {qrad_values.min():.6f} to {qrad_values.max():.6f}")
    print(f"Qrad mean: {qrad_values.mean():.6f}")

    # Plot the results
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.plot(x_coords, qrad_values, "bo-", linewidth=2, markersize=4)
    plt.xlabel("X Position (Cell Centers)")
    plt.ylabel("Qrad")
    plt.title(f"Qrad Distribution Along Horizontal Line (y = {y_mid:.3f})")
    plt.grid(True, alpha=0.3)
    plt.show()

    # Save the data to a file
    np.savetxt(
        "qrad_line_data.txt",
        np.column_stack([x_coords, qrad_values]),
        header="X_CellCenter Qrad_Value",
        delimiter=",",
        fmt="%.6f",
    )
    print("Data saved to 'qrad_line_data.txt'")

else:
    print("Error: 'Qrad' scalar field not found in the mesh")
    print(f"Available arrays: {mesh.array_names}")
