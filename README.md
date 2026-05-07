# 🌱 Optimal Sensor Placement UI

This repository contains the Streamlit-based UI developed for the Optimal Sensor Placement and Forecasting using Machine Learning project.

The application performs:
- Data validation
- Spatial interpolation
- Feature extraction
- PCA-based dimensionality reduction
- K-Means clustering
- Optimal sensor placement visualization
- Download of optimized sensor coordinates

---

# 📂 Project Structure

## `app.py`
Main Streamlit application file.

Responsibilities:
- Handles file uploads
- Displays UI components
- Executes the complete optimization pipeline
- Displays visualizations and outputs
- Provides CSV download functionality

---

## `validation.py`
Used for validating uploaded datasets.

Responsibilities:
- Verifies sensor count
- Matches sensor IDs across files
- Checks whether all sensors lie inside the field boundary polygon

---

## `grid.py`
Used for spatial grid generation.

Responsibilities:
- Creates spatial grid over the agricultural field
- Converts meter resolution into latitude/longitude spacing
- Generates polygon mask to retain only valid field points

---

## `interpolation.py`
Used for Kriging interpolation.

Responsibilities:
- Performs spatial interpolation on sensor observations
- Reconstructs continuous field-wide temperature and humidity maps
- Generates interpolated feature stacks

---

## `cell_features.py`
Used for statistical feature extraction.

Responsibilities:
- Computes:
  - Mean
  - Standard deviation
  - Range
- Extracts feature vectors for every grid cell

---

## `dimensionality.py`
Used for dimensionality reduction.

Responsibilities:
- Standardizes extracted features
- Applies PCA to reduce feature dimensionality while preserving variance

---

## `clustering.py`
Used for clustering and cluster evaluation.

Responsibilities:
- Performs K-Means clustering
- Evaluates optimal K using:
  - Silhouette Score
  - Davies–Bouldin Score
  - Inertia (Elbow Method)
- Automatically selects optimal cluster count

---

## `sensor_selection.py`
Used for optimal sensor placement.

Responsibilities:
- Identifies representative sensor locations from clusters
- Selects centroid positions from dominant cluster regions
- Generates final optimized sensor coordinates

---

# 📂 Required Input Files

## 1. `field_boundary.csv`

Contains field boundary coordinates in sequential polygon order.

Example:

| latitude | longitude |
|---|---|
| 45.3921 | 9.6962 |
| 45.3924 | 9.6968 |

---

## 2. `sensor_coordinates.csv`

Contains deployed sensor coordinates.

Example:

| sensor_id | latitude | longitude |
|---|---|---|
| 1 | 45.3918 | 9.6965 |

---

## 3. `sensor_hourly.csv`

Contains hourly sensor observations.

Example:

| sensor_id | timestamp | temperature | humidity |
|---|---|---|---|
| 1 | 2024-01-01 00:00 | 12.3 | 78.2 |

---

# 🛠️ Libraries Used

## Core Libraries
- numpy
- pandas
- matplotlib
- seaborn

## Machine Learning
- scikit-learn

## Spatial Processing
- shapely
- pykrige
- scipy

## UI Development
- streamlit

---

# ⚙️ Setup Process

## Step 1: Clone Repository

```bash
git clone https://github.com/nayan0413/Optimal-Sensor-Placement-and-Forecasting-using-Machine-Learning.git
```

---

## Step 2: Navigate to UI Folder

```bash
cd Optimal-Sensor-Placement-and-Forecasting-using-Machine-Learning/ui
```

---

## Step 3: Create Virtual Environment (Optional but Recommended)

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install manually:

```bash
pip install streamlit numpy pandas matplotlib seaborn scikit-learn shapely pykrige scipy
```

---

# ▶️ Running the Application

Run the Streamlit application using:

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

# 🗺️ Output Visualizations

The UI generates:
- Initial sensor placement map
- Cluster evaluation plots
- Final clustered field map
- Optimal sensor placement map

---

# 📥 Output Files

The final optimized sensor coordinates can be downloaded as:

```text
optimal_sensor_coordinates.csv
```

---

# 🚀 Future Improvements

- Integrating Google Maps/OpenStreetMap-based field boundary drawing
- Real-time sensor data streaming
- Forecasting integration directly into the UI
- Support for additional environmental variables
- Interactive GIS-based visualization

---

# 👨‍💻 Authors

- Nayan Singhania (BT22ECE115)
- Prasanna Athawale (BT22ECE023)
- Anjal Mallick (BT22ECE113)
- Yash Rahate (BT22ECE007)

---

# 🔗 GitHub Repository

https://github.com/nayan0413/Optimal-Sensor-Placement-and-Forecasting-using-Machine-Learning
