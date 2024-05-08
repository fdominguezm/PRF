from .gaussian import sample_gaussian
import numpy as np

class RLWE:
    def __init__(self, n, q, alpha):
        self.n = n
        self.q = q
        self.alpha = alpha

    def generate_sample(self):
        a = np.random.randint(0, self.q, self.n)  # Uniformly random polynomial coefficients
        e = sample_gaussian(self.alpha * self.q, self.n)  # Sample from discrete Gaussian
        return a, np.mod(a * self.s + e, self.q)  # Return (a, a*s + e) mod q

    def decision_rlwe(self, samples):
        # Implementation of decision RLWE
        pass

    def search_rlwe(self):
        # Implementation of search RLWE
        pass
