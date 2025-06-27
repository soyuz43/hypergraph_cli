# phases/mahalanobis.py

import numpy as np
from sklearn.covariance import EmpiricalCovariance

def train_mahalanobis_model(embeddings: list[np.ndarray]) -> EmpiricalCovariance:
    """
    Fit a Mahalanobis model using the provided embedding vectors.
    """
    matrix = np.stack(embeddings)
    model = EmpiricalCovariance()
    model.fit(matrix)
    return model

def compute_mahalanobis_distance(model: EmpiricalCovariance, vector: np.ndarray) -> float:
    """
    Compute Mahalanobis distance from the given vector to the trained model distribution.
    """
    return model.mahalanobis([vector])[0]
