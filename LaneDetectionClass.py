
import numpy as np
import math
class DetectLaneLines:
    #Class variables
    lane_width=3.5
    window_width=0.15
    window_height = 2.5
    y_axis_slide_limit=math.ceil(lane_width / window_width)
    
    def __init__(self,point_cloud):
       self.point_cloud=point_cloud
       self.final_left_line=[]
       self.final_right_line=[]
       
    def find_pairs(self, potential_line_XY_left, potential_line_XY_Right,right_line, left_line, base_Y):
        """
        Takes openetial left and right lane points over a given x interval as inputs and identifies actual lane points 
        among them by: 
        1. form all possible pairs of left and right lane points.
        2. Select the pair representing the actual lane lines by comparing the distance between the paired points with 
        the standard lane width relaxed by some tolerance value. 
        """
        tolerance = 0.055
        pairs = []
        for x1, y1 in potential_line_XY_left:
            for x2, y2 in potential_line_XY_Right:
                if abs(y1 - y2) >= (DetectLaneLines.lane_width - tolerance) and abs(y1 - y2) <= (DetectLaneLines.lane_width + tolerance):
                    pairs.append(((x1, y1), (x2, y2)))
        if pairs:
            (x1, y1), (x2, y2) = pairs[0]
            right_line.append((x1, y1))
            left_line.append((x2, y2))
            new_base_Y = (y1 + y2) / 2
            return right_line, left_line, new_base_Y
        else:
            return right_line, left_line, base_Y

    def find_line_points_in_window(self, lowerX, upperX, LowerY, UpperY, intensity_threshold=0.0235):
        """
        Finds lane points within a specified window.

        Parameters:
        lowerX (float): The lower X boundary of the window.
        upperX (float): The upper X boundary of the window.
        LowerY (float): The lower Y boundary of the window.
        UpperY (float): The upper Y boundary of the window.
        intensity_threshold (float): The threshold for considering a point as a potential lane point.

        Returns:
        tuple: Average potential lane point X and Y coordinates, or (None, None) if no points are found.
        """

        window_points_indices = np.where((self.point_cloud[:, 0] >= lowerX) & (self.point_cloud[:, 0] <= upperX) & (self.point_cloud[:, 1] >= LowerY) & (self.point_cloud[:, 1] <= UpperY))
        window_points = self.point_cloud[window_points_indices]
        potential_line_point_Indices = np.where((window_points[:, 3] >= intensity_threshold))
        if np.any(potential_line_point_Indices):
            potential_line_points = window_points[potential_line_point_Indices]
            avg_potential_Line_Point_X = np.mean(potential_line_points[:, 0])
            avg_potential_Line_Point_Y = np.mean(potential_line_points[:, 1])
            return avg_potential_Line_Point_X, avg_potential_Line_Point_Y
        else:
            return None, None
    
    def direction_wise_line_detection(self,base_Y,x_val,base_Y_history):
        """
        Detects potential lane points by scanning(sliding windows) across the road both length 
        wise(x-axis) and width wise(y-axis). For each x-axis interval, the method slides a 
        window along the y-axis to find lane points, building the list of potential lane points
        for both left and right lanes. It then calls find_pairs function to find the actual line points
        among the potential line points. Overall, the method returns the compiled lists of lane points for 
        the left and right lanes within the input x-axis range(x_val). See the "lane_detection" method for 
        input x-axis ranges.
        """
        right_line = []
        left_line = []
        # Append the initial base_Y value
        base_Y_history.append(base_Y)
        
        for i in range(len(x_val) - 1):   #This outer loop ensures scanning along the x-axis i.e. along the length of the road. The inner loop scans along the y-axis i.e. width of the raod for each x-axis interval         
            potential_lane_XY_left = []
            potential_lane_XY_Right = []
        
            # Window Boundaries
            win_lowerX = x_val[i]
            if x_val[i]<0:
                win_upperX = x_val[i - 1]   # Ensures movement in negative x-axis direction
            else:
                win_upperX = x_val[i + 1]
            winL_lowerY = base_Y - DetectLaneLines.window_width / 2
            winL_upperY = base_Y + DetectLaneLines.window_width / 2
            winR_lowerY = base_Y - DetectLaneLines.window_width / 2
            winR_upperY = base_Y + DetectLaneLines.window_width / 2
            
            for j in range(DetectLaneLines.y_axis_slide_limit):
                xL, yL = self.find_line_points_in_window(win_lowerX, win_upperX, winL_lowerY, winL_upperY)
                if xL is not None and yL is not None:
                    potential_lane_XY_left.append((xL, yL))

                xR, yR = self.find_line_points_in_window(win_lowerX, win_upperX, winR_lowerY, winR_upperY)
                if xR is not None and yR is not None:
                    potential_lane_XY_Right.append((xR, yR))
                # Slide the Left window to the left and the right window to the right
                winL_lowerY -= DetectLaneLines.window_width
                winL_upperY -= DetectLaneLines.window_width
                winR_lowerY += DetectLaneLines.window_width                
                winR_upperY += DetectLaneLines.window_width

            if potential_lane_XY_left and potential_lane_XY_Right:
                right_line, left_line, base_Y = self.find_pairs(potential_lane_XY_left, potential_lane_XY_Right,right_line, left_line, base_Y)
                # Append the updated base_Y value after find_pairs call
                base_Y_history.append(base_Y)
        return right_line, left_line,base_Y_history

    def line_detection(self):
        """
        This function splits the point cloud into two segments, one with positive x values and the other with 
        negative x values. It then calls "direction_wise_lane_detection" function to find line points on each segment. 
        After finding these points, it concatenates the line points from both parts to form the complete lines.
        """
        base_Y = 0
        base_Y_history_positive=[]
        base_Y_history_negitive=[]
        max_x = 150
        min_x = -150
        num_samples = int((max_x - min_x)/DetectLaneLines.window_height) + 1
        x_val = np.linspace(min_x, max_x, num=int(num_samples))
        x_val_positive = x_val[x_val >= 0]
        x_val_negative = x_val[x_val < 0]
        x_val_negative = np.flip(x_val[x_val < 0])


        right_line_negative,left_line_negative,base_Y_history_negitive=self.direction_wise_line_detection(base_Y,x_val_negative,base_Y_history_negitive) 
        right_line_positive,left_line_positive,base_Y_history_positive=self.direction_wise_line_detection(base_Y,x_val_positive,base_Y_history_positive) 

        self.final_right_line=right_line_positive+right_line_negative
        self.final_left_line=left_line_positive+left_line_negative


