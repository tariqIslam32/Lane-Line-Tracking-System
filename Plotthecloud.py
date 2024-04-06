import plotly.graph_objects as go
import numpy as np


bin_path="/home/tariq/Desktop/AssembledProperly/FinalProject6/Bins/6.bin"
pointCldBin = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 5)   
pointCldBin[:, 3] = pointCldBin[:, 3] / 255 

points=pointCldBin[:,:4]

# Extracting x, y, z, and intensity
x, y, z, intensity = points.T

# Create a scatter plot
fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=intensity,  # Set color to the intensity values
        colorscale='Greys',  # Greyscale colors
        opacity=0.8
    )
)])

# Set titles and labels
fig.update_layout(
    title="Point Cloud Visualization with Intensity",
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    )
)

# Show the plot
fig.show()