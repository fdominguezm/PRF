import numpy as np

class RLWE_PRF:
    def __init__(self, n, p, q, m, k):
        self.n = n  # Dimension of the lattice
        self.p = p  # Modulus
        self.q = q  # Larger modulus, q >= p
        self.m = m  # Polynomial degree
        self.k = k  # Input length
        
        # Generate A matrix (uniformly random)
        self.A = np.random.randint(0, q, size=(n, m))

        # Generate S matrices (uniformly random)
        self.S = [np.random.randint(0, q, size=(n, n)) for _ in range(k)]
    
    def eval(self, x):
        assert len(x) == self.k, "Input length must match k"
        
        # Compute F(x)
        productory = np.identity(self.n)

        for i, xi in enumerate(x):
            if xi == 1:
                productory = np.dot(productory, self.S[i]) % self.p

        result = np.dot(self.A.T, productory) % self.p

        return result % self.p

# Example usage:
n = 128   # Dimension of the lattice
p = 2     # Modulus
q = 4096  # Larger modulus, q >= p
m = 256   # Polynomial degree
k = 16    # Input length

rlwe_prf = RLWE_PRF(n, p, q, m, k)
x = np.random.randint(0, 2, size=k).tolist()  # Input (binary representation as list)
print("\nX = ",x)
output = rlwe_prf.eval(x)
print("\nF(x) =", output)

