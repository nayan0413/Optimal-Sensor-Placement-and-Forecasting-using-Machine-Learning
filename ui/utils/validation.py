import pandas as pd
from shapely.geometry import Point, Polygon


def load_data(field_file, coord_file, data_file):
    field_file.seek(0)
    coord_file.seek(0)
    data_file.seek(0)

    df_field = pd.read_csv(field_file)
    df_coord = pd.read_csv(coord_file)
    df_data = pd.read_csv(data_file)
    return df_field, df_coord, df_data


def check_sensor_count(df_coord, expected_count):
    actual_count = df_coord.shape[0]
    return actual_count == expected_count, actual_count


def check_sensor_id_match(df_coord, df_data):
    coord_ids = set(df_coord['sensor_id'])
    data_ids = set(df_data['sensor_id'])

    missing_in_data = coord_ids - data_ids
    missing_in_coord = data_ids - coord_ids

    return missing_in_data, missing_in_coord


def check_sensors_inside_polygon(df_field, df_coord):
    polygon_coords = list(zip(df_field['longitude'], df_field['latitude']))
    polygon = Polygon(polygon_coords)

    outside_sensors = []

    for _, row in df_coord.iterrows():
        point = Point(row['longitude'], row['latitude'])
        
        if not polygon.covers(point):
            outside_sensors.append(row['sensor_id'])

    return outside_sensors