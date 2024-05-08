# FIRST VERSION
# import numpy as np
# from numpy.linalg import norm

# # Parameters
# q = 12289  # modulus
# n = 256    # security parameter (polynomial degree)
# σ = 8.0    # standard deviation

# # Sample secret key and error
# def sample_secret_key():
#     return np.random.randint(0, q, n)

# def sample_error():
#     return np.random.normal(0, σ, n)

# # Generate public key
# def generate_public_key(secret_key, error):
#     return (secret_key + error) % q

# # Evaluate PRF
# def evaluate_prf(secret_key, public_key, input_vector):
#     return np.dot(secret_key, input_vector) % q

# # Example usage
# input_vector = np.random.randint(0, q, n)  # Input to PRF
# secret_key = sample_secret_key()  # Sample secret key
# error = sample_error()  # Sample error
# public_key = generate_public_key(secret_key, error)  # Generate public key
# prf_value = evaluate_prf(secret_key, public_key, input_vector)  # Evaluate PRF

# print("Input Vector:", input_vector)
# print("PRF Value:", prf_value)

# SECOND VERSION
# import numpy as np

# class LatticePRF:
#     def __init__(self, n, q):
#         self.n = n  # Dimension of the lattice
#         self.q = q  # Modulus

#         # Generate random lattice basis
#         self.B = np.random.randint(0, q, size=(n, n))

#     def keygen(self):
#         # Generate random secret key
#         self.s = np.random.randint(0, self.q, size=self.n)
#         # Compute public key
#         self.A = np.dot(self.s, self.B) % self.q

#     def evaluate(self, x):
#         # Ensure x is in Z_q^n
#         assert len(x) == self.n, "Input vector length must match lattice dimension"
#         assert all(0 <= xi < self.q for xi in x), "Input vector must be in Z_q^n"

#         # Compute PRF value
#         return np.dot(self.A, x) % self.q

# # Example usage
# n = 4  # Dimension of the lattice
# q = 17  # Modulus

# prf = LatticePRF(n, q)
# prf.keygen()

# x = np.random.randint(0, q, size=n)  # Input vector
# print("Input:", x)
# print("PRF value:", prf.evaluate(x))


# THIRD VERSION
# import numpy as np
# from numpy.polynomial.polynomial import Polynomial

# class RingLWEPRF:
#     def __init__(self, q, k, poly_deg):
#         self.q = q  # Modulus
#         self.k = k  # Degree of the polynomial
#         self.poly_deg = poly_deg  # Degree of the polynomial ring

#         # Generate random polynomial coefficients for the secret key
#         self.s_coeffs = np.random.randint(0, q, size=k+1)

#         # Generate random polynomial coefficients for the error
#         self.e_coeffs = np.random.randint(0, q, size=poly_deg)

#         # Generate random polynomial coefficients for the public key
#         self.a_coeffs = np.random.randint(0, q, size=(k+1, poly_deg))

#     def keygen(self):
#         # Compute the public key as a polynomial
#         self.a = Polynomial(self.a_coeffs.flatten() % self.q)

#     def evaluate(self, x):
#         # Ensure x is a polynomial of degree k
#         assert len(x) == self.k + 1, "Input polynomial degree must match k"

#         # Compute the PRF value
#         return (self.a * x).truncate(self.poly_deg).coef % self.q

# # Example usage
# q = 17  # Modulus
# k = 2   # Degree of the polynomial
# poly_deg = 5  # Degree of the polynomial ring

# prf = RingLWEPRF(q, k, poly_deg)
# prf.keygen()

# # Generate a random polynomial for evaluation
# x_coeffs = np.random.randint(0, q, size=k+1)
# x = Polynomial(x_coeffs)

# print("Input polynomial:", x)
# print("PRF value:", prf.evaluate(x))


# FOURTH VERSION
# import numpy as np

# class RLWE_PRF:
#     def __init__(self, n, p, q, m, k):
#         self.n = n  # Dimension of the lattice
#         self.p = p  # Modulus
#         self.q = q  # Larger modulus, q >= p
#         self.m = m  # Polynomial degree
#         self.k = k  # Input length
        
#         # Generate A matrix (uniformly random)
#         self.A = np.random.randint(0, q, size=(n, m))

#         # Generate S matrices (uniformly random)
#         self.S = [np.random.randint(0, q, size=(n, n)) for _ in range(k)]
    
#     def eval(self, x):
#         assert len(x) == self.k, "Input length must match k"


#     # # Compute F(x)
#     #     result = np.zeros((self.m, self.n))
#     #     for i, xi in enumerate(x):
#     #         result += np.dot(self.A.T, np.dot(self.S[i], xi))
        
#     #     return result % self.p
        
#         # Compute F(x)
#         # result = np.zeros((self.m, self.n))
#         productory = np.identity(self.n)

#         for i, xi in enumerate(x):
#             if xi == 1:
#                 productory = np.dot(productory, self.S[i])

#         result = np.dot(self.A.T, productory)

#         return result % self.p

# # Example usage:
# n = 128   # Dimension of the lattice
# p = 2     # Modulus
# q = 4096  # Larger modulus, q >= p
# m = 256   # Polynomial degree
# k = 16    # Input length

# rlwe_prf = RLWE_PRF(n, p, q, m, k)
# x = np.random.randint(0, 2, size=k).tolist()  # Input (binary representation as list)
# print("\nX = ",x)
# output = rlwe_prf.eval(x)
# print("\nF(x) =", output)

