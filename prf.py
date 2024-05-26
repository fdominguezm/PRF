import numpy as np
import numpy as np
from polynomial import Polynomial
from gaussian import sample_gaussian
import random

class RLWE_PRF:
    def __init__(self, p, q, n, k, alpha):

        self.p = p  # Modulus
        self.q = q  # Larger modulus, q >= p
        self.m = n**2  # m = poly(n) 
        self.k = k  # Input length
        
        # We choose a sigma with alpha*q >= 2n
        self.alpha = alpha
        self.sigma = np.ceil(alpha/np.sqrt(2*np.pi))

        # Set mod polynomial: x^n + 1
        self.mod_polynomial = Polynomial([1 for _ in range(n + 1)])
        aux = n - 1 
        while aux > 0:
            self.mod_polynomial[aux] = 0
            aux -= 1
                
    # Setup polynomial A
    def generate_a(self):
        q_a, a_polynomial = divmod(Polynomial([ (random.randint(0, self.q)) for _ in range(self.m + 1)]), self.mod_polynomial)
        return a_polynomial
    
    # Setup a number k of S polynomials 
    def generate_s(self):
        s_polynomials = []

        i = 0        
        while (i < self.k):

            ## Setup S polynomials
            q_s, s_polynomial = divmod(Polynomial([ (sample_gaussian(self.sigma) )  for _ in range(self.m + 1)]), self.mod_polynomial)
            s_polynomials.append(s_polynomial)

            i+=1
        
        return s_polynomials
    
    # Rounding according to the paper
    def round(self, x):
        x = np.round((self.p/self.q) * x ) % self.p
        return x

    def eval(self, x):
        assert len(x) == self.k, "Input length must match k"

        a_polynomial = self.generate_a()
        s_polynomials = self.generate_s()
        
        # Compute F(x)

        poly_productory = Polynomial(1)
        for i, xi in enumerate(x):

            # If the bit is 1 the multiply the ongoing productory with the Si polynomial
            if xi == 1: 
                # Make the polynomials mod x^n + 1 for the values to stay in the ring
                q, poly_productory = divmod((poly_productory * s_polynomials[i]), self.mod_polynomial)

                # # Make the coefficients mod p
                poly_productory = self.coefficients_mod_q(poly_productory)


        q_r, result = divmod((a_polynomial * poly_productory), self.mod_polynomial)
        result = self.coefficients_mod_q(result)
        

        result = self.coefficients_rounded(result)

        return result
    
        # Make the coefficients of a polynomial mod p
    def coefficients_rounded(self, polynomial):

        for i in range(0,polynomial.degree + 1):
            polynomial[i] = self.round(polynomial[i])

        return polynomial

    # Make the coefficients of a polynomial mod p
    def coefficients_mod_q(self, polynomial):

        for i in range(0,polynomial.degree + 1):
            polynomial[i] = polynomial[i] % self.q

        return polynomial
    
# # Example 1 usage:

# p = 3     # Modulus
# q = 4096  # Larger modulus, q >= p
# m = 256   # Polynomial degree
# k = 16    # Input length

# # Example 2 usage:

p = 6    # Modulus
n = 2**4   # security parameter, some power of 2
k = 16    # Input length

q = int(np.round(p * k*(np.sqrt(n)*np.log2(n))**k*n**(np.log2(n)**0.1)))  # Larger modulus, q >= p

alpha = 5 * np.ceil(2*np.sqrt(n)/q) # αq >= 2√n has to be fulfilled
print('q', q, "type of", type(q))
rlwe_prf = RLWE_PRF(p, q, n, k, alpha)

x = np.random.randint(0, 2, size=k).tolist()  # Input (binary representation as list)
print("\nX = ",x)
output = rlwe_prf.eval(x)
print("\nF(x) =", output)