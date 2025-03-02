import numpy as np
import cmath

class CubicEquation:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.answers = self.solve_cubic()
        
    def solve_cubic(self):
        a, b, c, d = self.coefficients
        # Handle the case when a is zero (quadratic equation)
        if abs(a) < 1e-10:
            if abs(b) < 1e-10:  # Linear equation
                if abs(c) < 1e-10:  # Constant equation
                    return []
                return [-d/c]
            # Quadratic formula
            discriminant = c**2 - 4*b*d
            if discriminant >= 0:
                x1 = (-c + np.sqrt(discriminant)) / (2*b)
                x2 = (-c - np.sqrt(discriminant)) / (2*b)
                return [complex(x1, 0), complex(x2, 0)]
            else:
                x1 = complex(-c/(2*b), np.sqrt(-discriminant)/(2*b))
                x2 = complex(-c/(2*b), -np.sqrt(-discriminant)/(2*b))
                return [x1, x2]
        
        # Convert to depressed cubic form (x^3 + px + q = 0)
        b_a = b / a
        c_a = c / a
        d_a = d / a
        
        p = c_a - (b_a**2) / 3
        q = d_a - (b_a * c_a) / 3 + 2 * (b_a**3) / 27
        
        # Calculate the discriminant
        discriminant = (q**2 / 4) + (p**3 / 27)
        
        roots = []
        
        # Case 1: One real root and two complex conjugate roots
        if discriminant > 0:
            u = (-q/2 + cmath.sqrt(discriminant))**(1/3)
            v = (-q/2 - cmath.sqrt(discriminant))**(1/3)
            
            root1 = u + v - b_a/3
            root2 = -(u + v)/2 - b_a/3 + 1j * np.sqrt(3) * (u - v)/2
            root3 = -(u + v)/2 - b_a/3 - 1j * np.sqrt(3) * (u - v)/2
            
            roots = [root1, root2, root3]
            
        # Case 2: All roots are real and at least two are equal
        elif abs(discriminant) < 1e-10:
            u = -q/2
            if u >= 0:
                u = u**(1/3)
            else:
                u = -((-u)**(1/3))
                
            root1 = 2 * u - b_a/3
            root2 = -u - b_a/3
            
            roots = [root1, root2, root2]  # One simple, one double root
            
        # Case 3: All roots are real and distinct
        else:
            theta = cmath.acos(-q/2 * np.sqrt(27/(-p**3)))
            
            root1 = 2 * np.sqrt(-p/3) * np.cos(theta/3) - b_a/3
            root2 = 2 * np.sqrt(-p/3) * np.cos((theta + 2*np.pi)/3) - b_a/3
            root3 = 2 * np.sqrt(-p/3) * np.cos((theta + 4*np.pi)/3) - b_a/3
            
            roots = [complex(root1, 0), complex(root2, 0), complex(root3, 0)]
            
        return roots