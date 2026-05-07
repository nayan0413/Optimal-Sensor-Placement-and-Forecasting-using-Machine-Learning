import numpy as np
from shapely.geometry import Point, Polygon


def create_grid(df_field, cell_size=5):

    polygon_coords = list(zip(df_field['longitude'], df_field['latitude']))
    polygon = Polygon(polygon_coords)

    lat_min = df_field['latitude'].min()
    lat_max = df_field['latitude'].max()
    lon_min = df_field['longitude'].min()
    lon_max = df_field['longitude'].max()

    lat_step = cell_size / 111000
    mean_lat = (lat_min + lat_max) / 2
    lon_step = cell_size / (111000 * np.cos(np.radians(mean_lat)))

    grid_lat = np.arange(lat_min, lat_max, lat_step)
    grid_lon = np.arange(lon_min, lon_max, lon_step)

    grid_lon_mesh, grid_lat_mesh = np.meshgrid(grid_lon, grid_lat)

    # mask for polygon
    mask = np.array([
        polygon.covers(Point(lon, lat))
        for lon, lat in zip(grid_lon_mesh.ravel(), grid_lat_mesh.ravel())
    ]).reshape(grid_lat_mesh.shape)

    return grid_lat_mesh, grid_lon_mesh, mask, polygon