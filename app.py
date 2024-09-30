# backend/app.py
from flask import Flask, jsonify, request
import numpy as np  # Make sure this line is included
from flask_cors import CORS
import math 
from cardano_method import CubicEquation
import logging
from matrix_operations import add_matrix, subtract_matrix, multiply_matrix, claculate_determeinant, invert_matrix
from numpy import array, linalg

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')  # Add this route for the root URL
def home():
    return "Welcome to the Math App!"  # Response for the root URL

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')

    if operation == 'add':
        return jsonify({"result": round(a + b, 2)})
    elif operation == 'subtract':
        return jsonify({"result": round(a - b, 2)})
    elif operation == 'multiply':
        return jsonify({"result": round(a * b, 2)})
    elif operation == 'divide':
        if b == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        return jsonify({"result": round(a / b, 2)})
    elif operation == 'exponent':
        return jsonify({"result":round(a ** b, 2)})
    elif operation == 'sqrt':
        if a < 0:
            return jsonify({"error": "Cannot take square root of a negative number"}), 400
        return jsonify({"result": round(math.sqrt(a), 2)})
    else:
        return jsonify({"error": "Invalid operation"}), 400

def solve_quadratic(a, b, c):
    """
    Solves the quadratic equation ax^2 + bx + c = 0
    Returns a tuple with the two solutions (x1, x2)
    """
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None  # No real solutions
    elif discriminant == 0:
        x = -b / (2*a)
        return (x, x)
    else:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return (round(x1, 2), round(x2, 2))

@app.route('/solve_quadratic', methods=['POST'])
def quadratic_solver():
    data = request.json
    logging.debug(f"Received data for quadratic solver: {data}")
    
    try:
        a = float(data.get('a'))
        b = float(data.get('b'))
        c = float(data.get('c'))
        logging.debug(f"Parsed coefficients: a={a}, b={b}, c={c}")
    except (TypeError, ValueError) as e:
        logging.error(f"Invalid input for quadratic solver: {str(e)}")
        return jsonify({'error': 'Invalid input. Please provide numeric values for a, b, and c.'}), 400
    
    if a == 0:
        logging.error("Coefficient 'a' is zero")
        return jsonify({'error': 'The coefficient "a" cannot be zero for a quadratic equation.'}), 400
    
    try:
        solution = solve_quadratic(a, b, c)
        logging.debug(f"Quadratic solution: {solution}")
        
        if solution is None:
            return jsonify({'result': 'No real solutions'})
        else:
            return jsonify({'result': {'x1': solution[0], 'x2': solution[1]}})
    except Exception as e:
        logging.error(f"Error in quadratic_solver: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error in solving quadratic equation: {str(e)}'}), 500

@app.route('/solve_system', methods=['POST'])
def solve_system():
    data = request.json
    equation_count = data.get('equationCount')
    variable_count = data.get('variableCount')
    
    # Extract coefficients and constants
    A = []
    B = []
    for i in range(1, equation_count + 1):
        row = [data.get(f'a{i}{j}') for j in range(1, variable_count + 1)]
        A.append(row)
        B.append(data.get(f'd{i}'))

    try:
        A = np.array(A)
        B = np.array(B)

        # Check if the matrix is square
        if equation_count != variable_count:
            return jsonify({'error': 'The number of equations must match the number of variables for solving.'}), 400

        solution = np.linalg.solve(A, B)
        return jsonify({'result': {f'x{i+1}': round(solution[i], 2) for i in range(len(solution))}})
    except np.linalg.LinAlgError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def solve_polynomial(a, b, c, d):
    equation = CubicEquation([a, b, c, d])
    return equation.answers

@app.route('/solve_polynomial', methods=['POST'])
def polynomial_solver():
    data = request.json
    logging.debug(f"Received data for polynomial solver: {data}")
    
    try:
        a = float(data.get('a'))
        b = float(data.get('b'))
        c = float(data.get('c'))
        d = float(data.get('d'))
        logging.debug(f"Parsed coefficients: a={a}, b={b}, c={c}, d={d}")
    except (TypeError, ValueError) as e:
        logging.error(f"Invalid input for polynomial solver: {str(e)}")
        return jsonify({'error': 'Invalid input. Please provide numeric values for a, b, c, and d.'}), 400
    
    try:
        solution = solve_polynomial(a, b, c, d)
        logging.debug(f"Polynomial solution: {solution}")
        
        if solution is None or len(solution) == 0:
            return jsonify({'result': 'No real solutions'})
        else:
            result = {f'x{i+1}': round(float(x), 4) for i, x in enumerate(solution)}
            return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in polynomial_solver: {str(e)}", exc_info=True)
        return jsonify({'error': f'Error in solving polynomial equation: {str(e)}'}), 500

@app.route('/api/matrix/add', methods=['POST'])
def add_matrix_route():
    data = request.json
    logging.debug(f"Received data: {data}")
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
    if not matrix1 or not matrix2:
        return jsonify({'error': 'Missing matrix parameters'}), 400
    try:
        result = add_matrix(matrix1, matrix2)
        logging.debug(f"Result: {result}")
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in add_matrix: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/matrix/subtract', methods=['POST'])
def subtract_matrix_route():
    data = request.json
    logging.debug(f"Received data: {data}")
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
    if not matrix1 or not matrix2:
        return jsonify({'error': 'Missing matrix parameters'}), 400
    try:
        result = subtract_matrix(matrix1, matrix2)
        logging.debug(f"Result: {result}")
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in subtract_matrix: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/matrix/multiply', methods=['POST'])
def multiply_matrix_route():
    data = request.json
    logging.debug(f"Received data: {data}")
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
    if not matrix1 or not matrix2:
        return jsonify({'error': 'Missing matrix parameters'}), 400
    try:
        result = multiply_matrix(matrix1, matrix2)
        logging.debug(f"Result: {result}")
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in multiply_matrix: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/matrix/determinant', methods=['POST'])
def determinant_matrix_route():
    data = request.json
    logging.debug(f"Received data: {data}")
    matrix = data.get('matrix1')  # Change this line
    
    if not matrix:
        return jsonify({'error': 'Missing matrix parameter'}), 400
    try:
        result = claculate_determeinant(matrix)
        logging.debug(f"Result: {result}")
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in determinant_matrix: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/matrix/invert', methods=['POST'])
def invert_matrix_route():
    data = request.json
    logging.debug(f"Received data: {data}")
    matrix = data.get('matrix1')  # Change this line
    
    if not matrix:
        return jsonify({'error': 'Missing matrix parameter'}), 400
    try:
        result = invert_matrix(matrix)
        logging.debug(f"Result: {result}")
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error in invert_matrix: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/solve-matrix', methods=['POST'])
def solve_matrix():
    data = request.json
    operation = data.get('operation')
    matrix1 = np.array(data.get('matrix1'))
    matrix2 = np.array(data.get('matrix2')) if 'matrix2' in data else None

    try:
        if operation == 'add':
            result = np.add(matrix1, matrix2)
        elif operation == 'subtract':
            result = np.subtract(matrix1, matrix2)
        elif operation == 'multiply':
            result = np.matmul(matrix1, matrix2)
        elif operation == 'determinant':
            result = np.linalg.det(matrix1)
        elif operation == 'inverse':
            result = np.linalg.inv(matrix1)
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        return jsonify({'result': result.tolist() if isinstance(result, np.ndarray) else float(result)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Backend is working"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)