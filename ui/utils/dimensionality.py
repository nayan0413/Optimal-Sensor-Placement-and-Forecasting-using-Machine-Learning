from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def preprocess_features(features):

    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    pca = PCA(n_components=0.98)
    features_pca = pca.fit_transform(features_scaled)

    return features_pca, scaler, pca