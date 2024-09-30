from app import solve_quadratic, system_solver, polynomial_solver
from matrix_operations import add_matrix, subtract_matrix, multiply_matrix, claculate_determeinant, invert_matrix

def test_quadratic_solver():
    print("Testing Quadratic Solver:")
    print(solve_quadratic(1, 5, 6))  # Should print (-2.0, -3.0)
    print(solve_quadratic(1, 2, 1))  # Should print (-1.0, -1.0)
    print(solve_quadratic(1, 0, 1))  # Should print None

def test_system_solver():
    print("\nTesting System Solver:")
    data = {
        'equationCount': 2,
        'variableCount': 2,
        'a1': 1, 'b1': 1, 'd1': 5,
        'a2': 2, 'b2': 1, 'd2': 7
    }
    print(system_solver().json)  # Should print {'result': {'x1': 3.0, 'x2': 2.0}}

def test_polynomial_solver():
    print("\nTesting Polynomial Solver:")
    data = {'a': 1, 'b': -6, 'c': 11, 'd': -6}
    print(polynomial_solver().json)  # Should print {'result': {'x1': 3.0, 'x2': 2.0, 'x3': 1.0}}

def test_matrix_operations():
    print("\nTesting Matrix Operations:")
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    print("Add:", add_matrix(matrix1, matrix2))
    print("Subtract:", subtract_matrix(matrix1, matrix2))
    print("Multiply:", multiply_matrix(matrix1, matrix2))
    print("Determinant:", claculate_determeinant(matrix1))
    print("Invert:", invert_matrix(matrix1))

if __name__ == "__main__":
    test_quadratic_solver()
    test_system_solver()
    test_polynomial_solver()
    test_matrix_operations()