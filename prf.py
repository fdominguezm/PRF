import numpy as np

class RLWE_PRF:
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


# Example 1 usage:
# n = 128   # Dimension of the lattice
# p = 2     # Modulus
# q = 4096  # Larger modulus, q >= p
# m = 256   # Polynomial degree
# k = 16    # Input length

# Example 2 usage:
n = 64   # Dimension of the lattice
p = 5     # Modulus
q = 10  # Larger modulus, q >= p
m = n**2   # m = poly(n)
k = 16    # Input length

rlwe_prf = RLWE_PRF(n, p, q, m, k)
x = np.random.randint(0, 2, size=k).tolist()  # Input (binary representation as list)
print("\nX = ",x)
output = rlwe_prf.eval(x)
print("\nF(x) =", output)
