import numpy as np
from pykrige.ok import OrdinaryKriging


def kriging_interpolation(lons, lats, values, grid_points):

    OK = OrdinaryKriging(
        lons,
        lats,
        values,
        variogram_model='spherical',
        verbose=False,
        enable_plotting=False
    )

    z, _ = OK.execute(
        'points',
        grid_points[:, 0],  # lon
        grid_points[:, 1]   # lat
    )

    return z


def build_stacks(df_data, df_coord, grid_points):

    # merge data
    df = df_data.merge(df_coord, on='sensor_id')

    # detect feature columns (numeric only)
    exclude_cols = ['sensor_id', 'timestamp', 'latitude', 'longitude']

    feature_cols = [
        col for col in df.columns
        if col not in exclude_cols and np.issubdtype(df[col].dtype, np.number)
    ]

    timestamps = sorted(df['timestamp'].unique())

    feature_stacks = {col: [] for col in feature_cols}

    for t in timestamps:

        df_t = df[df['timestamp'] == t]

        # skip if no data
        if df_t.shape[0] == 0:
            continue

        lons = df_t['longitude'].values
        lats = df_t['latitude'].values

        for col in feature_cols:

            values = df_t[col].values

            # 🔥 FIX: remove NaNs
            mask = ~np.isnan(values)

            values = values[mask]
            lons_clean = lons[mask]
            lats_clean = lats[mask]

            # 🔥 FIX: skip if insufficient points
            if len(values) < 3:
                continue

            grid_values = kriging_interpolation(
                lons_clean, lats_clean, values, grid_points
            )

            feature_stacks[col].append(grid_values)

    # remove empty features
    feature_stacks = {
        k: np.array(v) for k, v in feature_stacks.items() if len(v) > 0
    }
    
    # convert to numpy arrays
    for col in feature_cols:
        feature_stacks[col] = np.array(feature_stacks[col])

    return feature_stacks