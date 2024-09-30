import cmath

class CubicEquation:
    def __init__(self, coefficients):
        self.coefficients = coefficients
        self.answers = self.solve_cubic()

    def solve_cubic(self):
        a, b, c, d = self.coefficients

        # Calculate the discriminant
        delta0 = b**2 - 3*a*c
        delta1 = 2*b**3 - 9*a*b*c + 27*a**2*d

        # Calculate the discriminant of the cubic equation
        discriminant = (delta1**2 - 4*delta0**3) / -27*a**2

        # Calculate the complex cube roots of the discriminant
        C = cmath.sqrt(discriminant)

        # Calculate the three roots
        u = (-1 + cmath.sqrt(-3)) / 2
        roots = []
        for k in range(3):
            root = -(1/(3*a)) * (b + u**k * C + delta0 / (u**k * C))
            roots.append(root)

        # Return the real parts of the roots rounded to 2 decimal places
        return [round(root.real, 2) for root in roots]