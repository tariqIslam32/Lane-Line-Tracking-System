import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN
class PointCloudProcessor:
    def __init__(self, bin_path):
        self.bin_path = bin_path
        self.point_cloud = np.fromfile(self.bin_path, dtype=np.float32).reshape(-1, 5)
        self.point_cloud[:, 3] = self.point_cloud[:, 3] / 255 
        self.road_points= None

    def duplicate_and_outlier_removal(self):
        # Find unique rows (points) in the point cloud data
        _, indices = np.unique(self.point_cloud, axis=0, return_index=True)
        unique_point_cloud = self.point_cloud[indices]

        # OUTLIER REMOVAL
        # Create point cloud object
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(unique_point_cloud[:, :3])

        # Statistical Outlier Removal
        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=3, std_ratio=0.8)

        # Filter the point cloud array to keep only inliers
        denoised_point_cloud = unique_point_cloud[ind]
        # return denoised_point_cloud
        self.roadSeg(denoised_point_cloud)

    def roadSeg(self,denoised_point_cloud):
        """
        Apply RANSAC and DBSCAN to identify the main plane (road) in the point cloud.
        """
        pc_o3d = o3d.geometry.PointCloud()
        pc_o3d.points = o3d.utility.Vector3dVector(denoised_point_cloud[:, :3])  # Use only XYZ for RANSAC
        plane_model, inliersIdx = pc_o3d.segment_plane(distance_threshold=0.2, ransac_n=3, num_iterations=2000)
        road_points_inliers=denoised_point_cloud[inliersIdx]
    
        #Apply DBSCAN Clustering
        clustering = DBSCAN(eps=0.05, min_samples=40).fit(road_points_inliers[:, :3])
        labels = clustering.labels_
        # Extract the main cluster (assuming the road is the main cluster)
        self.road_points = road_points_inliers[labels == 0]
        
