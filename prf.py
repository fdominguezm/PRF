import numpy as np
import numpy as np
from sympy import poly,div, ZZ,rem
from sympy.abc import x
from polynomial import Polynomial


# class RLWE_PRF:
#     def __init__(self, n, p, q, m, k):
#         self.n = n  # Dimension of the lattice
#         self.p = p  # Modulus
#         self.q = q  # Larger modulus, q >= p
#         self.m = m  # Polynomial degree
#         self.k = k  # Input length
        
#         self.renew()
    
#     def eval(self, x):
#         assert len(x) == self.k, "Input length must match k"
        
#         # Compute F(x), x is a sequence of bits
#         productory = np.identity(self.n)

#         for i, xi in enumerate(x):
#             if xi == 1:
#                 productory = np.dot(productory, self.S[i])

#         result = np.dot(self.A.T, productory)
#         v_round = np.vectorize(self.round)
#         return v_round(result)

#     def round(self, x):
#         return np.round(self.p/self.q * x) % self.p

#     def renew(self):
#         # Generate A matrix (uniformly random)
#         self.A = np.random.randint(0, self.q, size=(self.n, self.m))

#         # Generate S matrices (uniformly random)
#         self.S = [np.random.randint(0, self.q, size=(self.n, self.n)) for _ in range(self.k)]




## Implementation Ring LWE


# class RLWE_PRF:
#     def __init__(self, n, p, q, m, k):
#         self.n = n  # Dimension of the lattice
#         self.p = p  # Modulus
#         self.q = q  # Larger modulus, q >= p
#         self.m = m  # Polynomial degree
#         self.k = k  # Input length
#         self.mod_polynomial = x**self.n + 1
    

#         # Setup polynomial A

#         a_polynomial = sum((np.random.randint(0, q ) ) * x**i for i in range(self.m)) 
#         self.a_polynomial = rem(a_polynomial, self.mod_polynomial, domain = ZZ)

#         self.s_polynomials = []

#         i = 0        
#         while (i < self.k):

#             ## Setup S polynomials
#             s_polynomial = sum((np.random.randint(0, 99999999) ) * x**i for i in range(self.m))
#             self.s_polynomials.append(rem(s_polynomial, self.mod_polynomial, domain=ZZ))

#             ## Increment i
#             i+=1


    
#     def eval(self, x):
#         assert len(x) == self.k, "Input length must match k"
        
#         # Compute F(x)

#         poly_productory_started = False
#         for i, xi in enumerate(x):
#             if xi == 1: 
#                 if poly_productory_started:
#                     poly_productory = poly(poly_productory * self.s_polynomials[i] )
#                 else:
#                     poly_productory = poly(self.s_polynomials[i] )
#                     poly_productory_started = True

#         result = poly(self.a_polynomial * poly_productory)

#         return result


class RLWE_PRF:
    def __init__(self, n, p, q, m, k):
        self.n = n  # Dimension of the lattice
        self.p = p  # Modulus
        self.q = q  # Larger modulus, q >= p
        self.m = m  # Polynomial degree
        self.k = k  # Input length
        self.mod_polynomial = Polynomial([1 for _ in range(self.m + 2)])
        aux = self.m - 2
        while aux > 0:
            self.mod_polynomial[aux] = 0
            aux -= 1
        
        # Setup polynomial A
        q_a, self.a_polynomial = divmod(Polynomial([ (np.random.randint(0, q )) for _ in range(self.m)]), self.mod_polynomial)

        # Setup a number k of S polynomials 
        self.s_polynomials = []

        i = 0        
        while (i < self.k):

            ## Setup S polynomials
            q_s, s_polynomial = divmod(Polynomial([ (np.random.randint(0, 9999999 )) % self.p for _ in range(self.m)]),self.mod_polynomial)
            self.s_polynomials.append(s_polynomial)

            i+=1

    def eval(self, x):
        assert len(x) == self.k, "Input length must match k"
        
        # Compute F(x)

        poly_productory = Polynomial(1)
        for i, xi in enumerate(x):
            # If the bit is 1 the multiply the ongoing productory with the Si polynomial
            if xi == 1: 
                # Make the polynomials mod x^n + 1 for the values to stay in the ring
                q, poly_productory = divmod((poly_productory * self.s_polynomials[i]), self.mod_polynomial)

                # Make the coefficients mod p
                poly_productory = self.coefficients_mod_p(poly_productory)

        q_r, result = divmod((self.a_polynomial * poly_productory), self.mod_polynomial)
        result = self.coefficients_mod_p(result)

        return result

    # Make the coefficients of a polynomial mod p
    def coefficients_mod_p(self, polynomial):

        for i in range(polynomial.degree + 1):
            polynomial[i] = polynomial[i] % self.p

        return polynomial
    
# # Example 1 usage:
n = 128   # Dimension of the lattice
p = 3     # Modulus
q = 4096  # Larger modulus, q >= p
m = 256   # Polynomial degree
k = 16    # Input length

# # Example 2 usage:
# n = 64   # Dimension of the lattice
# p = 5     # Modulus
# q = 10  # Larger modulus, q >= p
# m = n**2   # m = poly(n)
# k = 16    # Input length

rlwe_prf = RLWE_PRF(n, p, q, m, k)
x = np.random.randint(0, 2, size=k).tolist()  # Input (binary representation as list)
print("\nX = ",x)
output = rlwe_prf.eval(x)
print("\nF(x) =", output)