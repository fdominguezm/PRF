import numpy as np

def sample_gaussian(sigma, size):
    # Sample from a Gaussian distribution with standard deviation sigma
    return np.random.normal(scale=sigma, size=size)
