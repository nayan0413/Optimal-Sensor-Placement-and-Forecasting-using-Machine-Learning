import numpy as np


def compute_cell_features(feature_stacks):

    feature_list = []

    for feature_name, stack in feature_stacks.items():

        # stack shape: (time, grid_points)

        mean = np.mean(stack, axis=0)
        std = np.std(stack, axis=0)
        range_ = np.max(stack, axis=0) - np.min(stack, axis=0)

        feature_list.append(mean)
        feature_list.append(std)
        feature_list.append(range_)

    # shape → (features, grid_points)
    features = np.array(feature_list)

    # transpose → (grid_points, features)
    features = features.T

    return features