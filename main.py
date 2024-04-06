import numpy as np
import os
from data_visualize import Vis
from PointCloudProcessor import PointCloudProcessor
from LaneDetectionClass import DetectLaneLines
from LaneLinesProcessor import LaneLinesProcessor
import time

def main():
    data_folder = "./PointCloud"
    lane_folder = "./Output"

    # Get all filenames and sort them numerically
    filenames = os.listdir(data_folder)
    filenames.sort(key=lambda f: int(os.path.splitext(f)[0]))

    for filename in filenames:
        bin_path = os.path.join(data_folder, filename)

        # pc_processor = PointCloudProcessor(bin_path)
        # pc_processor.duplicate_and_outlier_removal()
        # road_points=pc_processor.road_points 

        # Read and process the point cloud data
        pointCldBin = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 5)
        pointCldBin[:, 3] = pointCldBin[:, 3] / 255  # Normalize Intensity values
        road_points = pointCldBin[:, :4]

        # Detect lane lines
        detect_lines = DetectLaneLines(road_points)
        detect_lines.line_detection()

        # Process detected lane lines
        fit_lines = LaneLinesProcessor(detect_lines.final_left_line, detect_lines.final_right_line)
        fit_lines.calculate_lane_coefficients()

        # Write lane parameters to file
        output_filename = os.path.join(lane_folder, os.path.basename(bin_path).replace('.bin', '.txt'))
        fit_lines.write_lane_param_to_file(fit_lines.coeff_left, fit_lines.coeff_right, output_filename)

        # Visualize the fitted lane lines on the denoised point cloud
        vis = Vis(data_folder, lane_folder)
        vis.set_current_file(filename)
        vis.visualize()


if __name__ == "__main__":
    main()
