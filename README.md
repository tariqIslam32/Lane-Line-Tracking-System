### Seoul Robotics Coding Assignment: Ego Lane Detection
### Overview
This project focuses on Ego Lane Detection using point cloud data. The main objective is to accurately detect and analyze lane lines using advanced processing techniques.

### Directory Structure
PointCloud: This directory contains the point cloud data in .bin format.
Sample_output: Here, you'll find .txt files with the lane line coefficients for both left and right lane lines.
### Execution Instructions
Run main.py to display the sample output. This script is the entry point for the lane detection process.
### Technical Notes
The PointCloudProcessor class has been initially implemented for point cloud data processing. However, due to the need for parameter tuning to optimize data retention, this class is currently not in use.
To ensure consistent performance, direct lane detection methods have been applied, bypassing the PointCloudProcessor class.
It is important to note that certain point cloud files, such as point_cloud_9.bin, may achieve better results with alternative parameter settings different from those currently employed in the code.