from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import numpy as np


def evaluate_k(features, k_range=range(2, 16)):

    sil_scores = []
    db_scores = []
    inertias = []
    logs = []

    for k in k_range:

        km = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = km.fit_predict(features)

        sil = silhouette_score(features, labels)
        db = davies_bouldin_score(features, labels)

        sil_scores.append(sil)
        db_scores.append(db)
        inertias.append(km.inertia_)

        logs.append(f"k={k} | silhouette={sil:.4f} | DB={db:.4f} | inertia={km.inertia_:.1f}")

    return {
        "k": list(k_range),
        "silhouette": sil_scores,
        "db_score": db_scores,
        "inertia": inertias,
        "logs": logs
    }


def select_best_k(results):

    sil = np.array(results["silhouette"])
    db = np.array(results["db_score"])
    iner = np.array(results["inertia"])

    sil_norm = (sil - sil.min()) / (sil.max() - sil.min() + 1e-9)
    db_norm = (db.max() - db) / (db.max() - db.min() + 1e-9)
    iner_norm = (iner.max() - iner) / (iner.max() - iner.min() + 1e-9)

    combined = sil_norm + db_norm + iner_norm

    return results["k"][np.argmax(combined)]


def perform_clustering(features, k):

    kmeans = KMeans(n_clusters=k, n_init=30, random_state=42)
    labels = kmeans.fit_predict(features)

    return labels, kmeans