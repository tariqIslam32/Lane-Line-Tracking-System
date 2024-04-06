### Ego Lane Detection

### Overview
This project focuses on Ego Lane Detection using point cloud data. The main objective is to accurately detect and analyze lane lines using advanced processing techniques.

### Directory Structure
PointCloud: This directory contains the point cloud data in .bin format.

Sample_output: Here, you'll find .txt files with the lane line coefficients for both left and right lane lines.
### Execution Instructions
Run main.py to display the sample output. This script is the entry point for the lane detection process.
### Required Libraries
open3d==0.16.0

numpy==1.22.4

matplotlib==3.6.2

pynput==1.7.6

scikit-learn==1.3.2

scipy==1.10.1

### Technical Notes
The PointCloudProcessor class has been initially implemented for point cloud data processing. However, due to the need for parameter tuning to optimize data retention, this class is currently not in use.
To ensure consistent performance, direct lane detection methods have been applied, bypassing the PointCloudProcessor class. Find details in the attached report.
