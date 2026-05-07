import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

from utils.validation import (
    load_data,
    check_sensor_count,
    check_sensor_id_match,
    check_sensors_inside_polygon
)

from utils.grid import create_grid
from utils.interpolation import build_stacks
from utils.cell_features import compute_cell_features
from utils.dimensionality import preprocess_features
from utils.clustering import evaluate_k, select_best_k, perform_clustering
from utils.sensor_selection import select_sensor_locations

# --- Page config ---
st.set_page_config(page_title="Sensor Optimizer", layout="wide")

# --- Title ---
st.title("🌱 Sensor Placement Optimization Tool")

# --- Sidebar ---
st.sidebar.header("📥 Upload Inputs")

# 1. Field boundary
field_file = st.sidebar.file_uploader(
    "Upload Field Boundary CSV (latitude, longitude)", type=["csv"]
)

# 2. Sensor coordinates
sensor_coord_file = st.sidebar.file_uploader(
    "Upload Sensor Coordinates CSV (sensor_id, latitude, longitude)", type=["csv"]
)

# 3. Sensor time data
sensor_data_file = st.sidebar.file_uploader(
    "Upload Sensor Time Data CSV (sensor_id, timestamp, ...)", type=["csv"]
)

# 4. Sensor count input
expected_sensors = st.sidebar.number_input(
    "Enter Number of Sensors",
    min_value=1,
    step=1
)

st.sidebar.markdown("---")

# --- Buttons ---
validate_btn = st.sidebar.button("✅ Validate Data")
run_btn = st.sidebar.button("🚀 Run Optimization")

# --- Main Output Area ---
st.header("📊 Output")

# --- Show uploaded data preview (very useful) ---
if field_file is not None:
    st.subheader("Field Boundary Preview")
    df_field = pd.read_csv(field_file)
    st.dataframe(df_field)

if sensor_coord_file is not None:
    st.subheader("Sensor Coordinates Preview")
    df_coord = pd.read_csv(sensor_coord_file)
    st.dataframe(df_coord)

if sensor_data_file is not None:
    st.subheader("Sensor Data Preview")
    df_data = pd.read_csv(sensor_data_file)
    st.dataframe(df_data.head())

# --- Validation placeholder ---
if validate_btn:
    if field_file and sensor_coord_file and sensor_data_file:

        df_field, df_coord, df_data = load_data(
            field_file, sensor_coord_file, sensor_data_file
        )

        st.subheader("🔍 Validation Results")

        # 1. Sensor count
        valid_count, actual_count = check_sensor_count(df_coord, expected_sensors)

        if valid_count:
            st.success(f"✔ Sensor count matches: {actual_count}")
        else:
            st.error(f"❌ Sensor count mismatch: expected {expected_sensors}, found {actual_count}")

        # 2. Sensor ID matching
        missing_data, missing_coord = check_sensor_id_match(df_coord, df_data)

        if not missing_data and not missing_coord:
            st.success("✔ Sensor IDs match across files")
        else:
            if missing_data:
                st.error(f"❌ Missing in sensor data: {missing_data}")
            if missing_coord:
                st.error(f"❌ Missing in coordinates: {missing_coord}")

        # 3. Inside polygon check
        outside = check_sensors_inside_polygon(df_field, df_coord)

        if not outside:
            st.success("✔ All sensors lie inside field")
        else:
            st.error(f"❌ Sensors outside field: {outside}")

    else:
        st.warning("⚠ Please upload all files before validation")

# --- Optimization placeholder ---
if run_btn:

    if field_file and sensor_coord_file and sensor_data_file:

        try:
            df_field, df_coord, df_data = load_data(
                field_file, sensor_coord_file, sensor_data_file
            )

            # ------------------ GRID ------------------
            st.subheader("📍 Grid Creation")

            grid_lat, grid_lon, mask, polygon = create_grid(df_field)

            grid_points = np.column_stack((
                grid_lon[mask],
                grid_lat[mask]
            ))

            st.write("Total grid points:", len(grid_points))

            # ------------------ INITIAL MAP ------------------
            st.subheader("🗺 Initial Sensor Placement")

            fig, ax = plt.subplots(figsize=(4, 4), dpi=120)

            # CLOSE POLYGON
            poly = Polygon(zip(df_field['longitude'], df_field['latitude']))
            x, y = poly.exterior.xy

            ax.plot(x, y, color='black', linewidth=1.5)

            # sensors
            ax.scatter(
                df_coord['longitude'],
                df_coord['latitude'],
                c='#1f77b4',
                s=50,
                edgecolors='black',
                linewidth=0.5,
                zorder=3
            )
            
            offset = 0.00007

            # labels (NOW VISIBLE)
            for _, row in df_coord.iterrows():
                ax.text(
                    row['longitude'],
                    row['latitude'] + offset,
                    str(int(row['sensor_id'])),
                    fontsize=5,
                    color='black',
                    ha='center',
                    va='bottom',
                    fontweight='bold',
                    zorder=4
                )

            # ✅ FIXES
            ax.set_aspect('equal')
            ax.ticklabel_format(style='plain', useOffset=False)

            # axis labels
            ax.set_xlabel("Longitude", fontsize=9)
            ax.set_ylabel("Latitude", fontsize=9)

            # ticks smaller
            ax.tick_params(axis='both', labelsize=8)

            # grid
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=False)

            # ------------------ INTERPOLATION ------------------
            st.subheader("⚙ Interpolation")

            feature_stacks = build_stacks(df_data, df_coord, grid_points)
            st.success("✔ Interpolation completed")

            # ------------------ FEATURES ------------------
            cell_features = compute_cell_features(feature_stacks)

            # ------------------ PCA ------------------
            X, _, _ = preprocess_features(cell_features)

            # ------------------ K EVALUATION ------------------
            st.subheader("📊 K Evaluation")

            results = evaluate_k(X)

            fig, axs = plt.subplots(1, 3, figsize=(10, 3), dpi=120)

            axs[0].plot(results["k"], results["silhouette"], marker="o")
            axs[0].set_title("Silhouette")

            axs[1].plot(results["k"], results["db_score"], marker="o")
            axs[1].set_title("DB Score")

            axs[2].plot(results["k"], results["inertia"], marker="o")
            axs[2].set_title("Elbow")

            plt.tight_layout()
            st.pyplot(fig)

            # ------------------ BEST K ------------------
            best_k = select_best_k(results)
            st.success(f"✔ Suggested K: {best_k}")

            k_final = best_k

            # ------------------ CLUSTERING ------------------
            labels, _ = perform_clustering(X, k_final)

            # rebuild grid
            label_grid = np.full(mask.shape, -1)
            label_grid[mask] = labels

            # ------------------ SENSOR SELECTION ------------------
            st.subheader("📍 Optimal Sensors")

            sensor_locations = select_sensor_locations(
                grid_lat,
                grid_lon,
                label_grid
            )

            st.write("Sensors required:", len(sensor_locations))

            # ------------------ FINAL MAP ------------------
            st.subheader("🗺 Optimal Sensor Placement")

            fig, ax = plt.subplots(figsize=(4, 4), dpi=120)

            # clusters
            sc = ax.scatter(
                grid_lon[mask],
                grid_lat[mask],
                c=labels,
                cmap='tab20',
                s=4,
                alpha=0.6
            )

            # boundary
            poly = Polygon(zip(df_field['longitude'], df_field['latitude']))
            x, y = poly.exterior.xy

            ax.plot(x, y, color='black', linewidth=1.5)

            # sensors
            ax.scatter(
                sensor_locations[:, 0],
                sensor_locations[:, 1],
                c='red',
                s=60,
                marker='X',
                edgecolors='black',
                zorder=4
            )

            # labels
            for i, (lon_s, lat_s) in enumerate(sensor_locations):
                ax.text(
                    lon_s,
                    lat_s,
                    str(i+1),
                    fontsize=7,
                    ha='center',
                    va='center',
                    color='red'
                )

            # FIXES
            ax.set_aspect('equal')
            ax.ticklabel_format(style='plain', useOffset=False)

            ax.set_xlabel("Longitude", fontsize=9)
            ax.set_ylabel("Latitude", fontsize=9)

            ax.tick_params(axis='both', labelsize=8)

            ax.grid(True, alpha=0.3)

            # colorbar
            cbar = plt.colorbar(sc, ax=ax, fraction=0.03, pad=0.02)
            cbar.ax.tick_params(labelsize=7)

            plt.tight_layout()
            st.pyplot(fig, use_container_width=False)
            
            import pandas as pd

            # ------------------ DOWNLOAD CSV ------------------

            # create dataframe
            df_output = pd.DataFrame({
                "sensor_id": range(1, len(sensor_locations) + 1),
                "latitude": sensor_locations[:, 1],
                "longitude": sensor_locations[:, 0]
            })

            # convert to CSV
            csv = df_output.to_csv(index=False).encode('utf-8')

            # download button
            st.download_button(
                label="📥 Download Sensor Coordinates CSV",
                data=csv,
                file_name="optimal_sensor_coordinates.csv",
                mime="text/csv"
            )

            # preview (optional but useful)
            st.dataframe(df_output)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    else:
        st.warning("⚠ Please upload all files")