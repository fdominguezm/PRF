import numpy as np

class LWE:
    def __init__(self, n, p, q, m, k):
        self.n = n  # Dimension of the lattice
        self.p = p  # Modulus
        self.q = q  # Larger modulus, q >= p
        self.m = m  # Polynomial degree
        self.k = k  # Input length
        
        self.renew()
    
    def eval(self, x):
        assert len(x) == self.k, "Input length must match k"
        
        # Compute F(x), x is a sequence of bits
        productory = np.identity(self.n)

        for i, xi in enumerate(x):
            if xi == 1:
                productory = np.dot(productory, self.S[i])

        result = np.dot(self.A.T, productory)
        v_round = np.vectorize(self.round)
        return v_round(result)

    def round(self, x):
        return np.round(self.p/self.q * x) % self.p

    def renew(self):
        # Generate A matrix (uniformly random)
        self.A = np.random.randint(0, self.q, size=(self.n, self.m))

        # Generate S matrices (uniformly random)
        self.S = [np.random.randint(0, self.q, size=(self.n, self.n)) for _ in range(self.k)]
