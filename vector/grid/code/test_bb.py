import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np

fig, ax = plt.subplots()
hex_cell = RegularPolygon((50, 50), numVertices=6, radius=10)
ax.add_patch(hex_cell)

# Test getting transformed vertices
path = hex_cell.get_path()
transform = hex_cell.get_patch_transform()
transformed_path = transform.transform_path(path)
vertices = transformed_path.vertices

print("Min X:", np.min(vertices[:, 0]))
print("Max X:", np.max(vertices[:, 0]))
print("Min Y:", np.min(vertices[:, 1]))
print("Max Y:", np.max(vertices[:, 1]))
