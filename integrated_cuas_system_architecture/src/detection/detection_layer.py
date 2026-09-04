import numpy as np

def synthetic_detection(true_xy, rng, position_std=12.0, detection_probability=0.96):
    """Return a generic noisy Cartesian detection or None."""
    if rng.random() > detection_probability:
        return None
    return np.asarray(true_xy, float) + rng.normal(0.0, position_std, 2)
