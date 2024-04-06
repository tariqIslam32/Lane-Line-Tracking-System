import matplotlib.pyplot as plt
import numpy as np
bin_path="/home/tariq/Desktop/AssembledProperly/MultipleWindows4/Bins/1.bin"
point_cloud =np.fromfile(bin_path, dtype=np.float32).reshape(-1, 5) 

# Extracting x and y coordinates
x_points = point_cloud[:, 0]  # All x coordinates
y_points = point_cloud[:, 1]  # All y coordinates

# Create the plot
plt.scatter(x_points, y_points)  # Plot the points

# Optionally, label your axes
plt.xlabel('X Axis')
plt.ylabel('Y Axis')

# Set the scale for the axes
plt.xlim([min(x_points) - 1, max(x_points) + 1])  # Set limits for x-axis
plt.ylim([min(y_points) - 1, max(y_points) + 1])  # Set limits for y-axis

# Show grid
plt.grid(True)

# Show the plot
plt.show()