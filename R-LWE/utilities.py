import numpy as np

def polynomial_addition(poly1, poly2):
    # Add two polynomials
    return np.mod(poly1 + poly2, poly1.size)

def polynomial_multiplication(poly1, poly2):
    # Multiply two polynomials
    return np.polymul(poly1, poly2)
