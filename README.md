🌱 Optimal Sensor Placement UI

This repository contains the Streamlit-based user interface developed for the Optimal Sensor Placement and Forecasting using Machine Learning project.

The application performs:

* Data validation
* Spatial grid generation
* Kriging interpolation
* Feature extraction
* PCA-based dimensionality reduction
* K-Means clustering
* Optimal sensor placement visualization
* Download of optimized sensor coordinates

⸻

📌 Features

* Upload field boundary, sensor coordinates, and sensor time-series data
* Validate sensor consistency and field boundary constraints
* Generate spatial field grids automatically
* Perform Kriging interpolation for microclimate reconstruction
* Determine optimal number of clusters using:
    * Silhouette Score
    * Davies–Bouldin Score
    * Elbow Method (Inertia)
* Visualize:
    * Initial sensor placement
    * Cluster evaluation plots
    * Final optimal sensor placement map
* Download optimized sensor coordinates as CSV

⸻

📂 Required Input Files

1. field_boundary.csv

Contains field boundary coordinates in sequential polygon order.

Example:

latitude	longitude
45.3921	9.6962
45.3924	9.6968

⸻

2. sensor_coordinates.csv

Contains deployed sensor coordinates.

Example:

sensor_id	latitude	longitude
1	45.3918	9.6965

⸻

3. sensor_hourly.csv

Contains hourly sensor observations.

Example:

sensor_id	timestamp	temperature	humidity
1	2024-01-01 00:00	12.3	78.2

⸻

🛠️ Libraries Used

The following Python libraries were used in this project:

Core Libraries

* numpy
* pandas
* matplotlib
* seaborn

Machine Learning

* scikit-learn

Spatial Processing

* shapely
* pykrige
* scipy

UI Development

* streamlit

⸻

⚙️ Setup Process

Step 1: Clone Repository

git clone https://github.com/nayan0413/Optimal-Sensor-Placement-and-Forecasting-using-Machine-Learning.git

⸻

Step 2: Navigate to UI Folder

cd Optimal-Sensor-Placement-and-Forecasting-using-Machine-Learning/ui

⸻

Step 3: Create Virtual Environment (Optional but Recommended)

Windows

python -m venv venv
venv\Scripts\activate

Linux / Mac

python3 -m venv venv
source venv/bin/activate

⸻

Step 4: Install Dependencies

pip install -r requirements.txt

If requirements.txt is not available, install manually:

pip install streamlit numpy pandas matplotlib seaborn scikit-learn shapely pykrige scipy

⸻

▶️ Running the Application

Run the Streamlit application using:

streamlit run app.py

The application will open automatically in your browser.

⸻

📊 Workflow of the UI

1. Upload field boundary, sensor coordinates, and sensor data
2. Validate uploaded datasets
3. Generate spatial field grid
4. Perform Kriging interpolation
5. Extract statistical features
6. Apply PCA for dimensionality reduction
7. Evaluate optimal K using clustering metrics
8. Perform K-Means clustering
9. Determine optimal sensor locations
10. Visualize results and download optimized coordinates

⸻

📈 Clustering Metrics Used

The optimal number of clusters is determined using:

* Silhouette Score
* Davies–Bouldin Index
* Inertia (Elbow Method)

A combined normalized score is used for automatic K selection.

⸻

🗺️ Output Visualizations

The UI generates:

* Initial sensor placement map
* Cluster evaluation plots
* Final clustered field map
* Optimal sensor placement map

⸻

📥 Output Files

The final optimized sensor coordinates can be downloaded as:

optimal_sensor_coordinates.csv

⸻

🚀 Future Improvements

* Integrating Google Maps/OpenStreetMap-based field boundary drawing
* Real-time sensor data streaming
* Forecasting integration directly into the UI
* Support for additional environmental variables
* Interactive GIS-based visualization

⸻

👨‍💻 Authors

* Nayan Singhania
* Project Team

⸻

🔗 GitHub Repository

https://github.com/nayan0413/Optimal-Sensor-Placement-and-Forecasting-using-Machine-Learning
