import numpy as np

class LaneLinesProcessor:
    def __init__(self, left_line_points, right_line_points):
        # Convert input lists to NumPy arrays
        self.left_line_points = np.array(left_line_points)
        self.right_line_points = np.array(right_line_points)
        self.coeff_left = None
        self.coeff_right = None

    def calculate_lane_coefficients(self):
        if self.left_line_points.size == 0:
            print("No data in left_lane_points")
            return
        else:
        # Calculate polynomial coefficients for both lanes
            self.coeff_left = np.polyfit(self.left_line_points[:, 0], self.left_line_points[:, 1], 3)
            self.coeff_right = np.polyfit(self.right_line_points[:, 0], self.right_line_points[:, 1], 3)

    @staticmethod
    def write_lane_param_to_file(left_line_params, right_line_params, output_file_path):
        # Format the lane parameters into strings
        left_line_str = ';'.join(map(str, left_line_params))
        right_line_str = ';'.join(map(str, right_line_params))

        # Write the formatted strings to the output file
        with open(output_file_path, 'w') as file:
            file.write(left_line_str + '\n')
            file.write(right_line_str + '\n')


