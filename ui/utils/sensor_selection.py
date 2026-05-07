import numpy as np
from scipy.ndimage import label


def select_sensor_locations(grid_lat, grid_lon, label_grid):

    sensor_locations = []

    unique_clusters = np.unique(label_grid)
    unique_clusters = unique_clusters[unique_clusters != -1]

    for cluster_id in unique_clusters:

        cluster_mask = (label_grid == cluster_id)

        labeled_regions, num_regions = label(cluster_mask)

        if num_regions == 0:
            continue

        region_sizes = [
            np.sum(labeled_regions == i)
            for i in range(1, num_regions + 1)
        ]

        largest_region_id = np.argmax(region_sizes) + 1
        largest_region_mask = (labeled_regions == largest_region_id)

        lat_points = grid_lat[largest_region_mask]
        lon_points = grid_lon[largest_region_mask]

        region_points = np.column_stack((lon_points, lat_points))

        centroid = np.mean(region_points, axis=0)

        distances = np.linalg.norm(region_points - centroid, axis=1)
        closest_idx = np.argmin(distances)

        sensor_locations.append(region_points[closest_idx])

    return np.array(sensor_locations)