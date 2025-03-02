from http.client import HTTPException
import numpy as np
from fastapi.responses import JSONResponse
from sympy import sympify, Symbol
from cardano_method import CubicEquation

async def evaluate_expression(data):
    expression = data.get('expression')
    
    if not expression:
        raise HTTPException(status_code=400, detail="No expression provided")

    try:
        expression = expression.replace('^', '**')
        x = Symbol('x')
        expr = sympify(expression)
        x_vals = np.linspace(-10, 10, 200)
        points = []
        f = lambda x_val: float(expr.subs(x, x_val))
        for x_val in x_vals:
            try:
                y_val = f(x_val)
                if isinstance(y_val, (int, float)) and np.isfinite(y_val):
                    points.append({'x': float(x_val), 'y': y_val})
            except (ValueError, TypeError, ZeroDivisionError):
                continue
        result = {
            'points': points,
            'expression': expression
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating expression: {str(e)}")

async def calculate(data):
    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')
    
    if operation == 'add':
        return JSONResponse(content={"result": round(a + b, 2)})
    elif operation == 'subtract':
        return JSONResponse(content={"result": round(a - b, 2)})
    elif operation == 'multiply':
        return JSONResponse(content={"result": round(a * b, 2)})
    elif operation == 'divide':
        if b == 0:
            return JSONResponse(content={"error": "Cannot divide by zero"}, status_code=400)
        return JSONResponse(content={"result": round(a / b, 2)})
    elif operation == 'exponent':
        return JSONResponse(content={"result": round(a ** b, 2)})
    elif operation == 'sqrt':
        if a < 0:
            return JSONResponse(content={"error": "Cannot take square root of a negative number"}, status_code=400)
        return JSONResponse(content={"result": round(np.sqrt(a), 2)})
    else:
        return JSONResponse(content={"error": "Invalid operation"}, status_code=400)

async def quadratic_solver(data):
    a = float(data.get('a'))
    b = float(data.get('b'))
    c = float(data.get('c'))
    
    if a == 0:
        return JSONResponse(content={'error': 'The coefficient "a" cannot be zero for a quadratic equation.'}, status_code=400)
    
    discriminant = b**2 - 4*a*c
    
    if discriminant < 0:
        return JSONResponse(content={'result': 'No real solutions'})
    elif discriminant == 0:
        x = -b / (2*a)
        return JSONResponse(content={'result': {'x1': round(x, 2), 'x2': round(x, 2)}})
    else:
        x1 = (-b + np.sqrt(discriminant)) / (2*a)
        x2 = (-b - np.sqrt(discriminant)) / (2*a)
        return JSONResponse(content={'result': {'x1': round(x1, 2), 'x2': round(x2, 2)}})

async def solve_system(data):
    equation_count = int(data.get('equationCount', 0))
    variable_count = int(data.get('variableCount', 0))
    
    if equation_count != variable_count:
        return JSONResponse(
            content={"error": "Number of equations must match number of variables"}, 
            status_code=400
        )
    
    # Extract coefficients and constants
    A = []
    B = []
    for i in range(1, equation_count + 1):
        row = [float(data.get(f'a{i}{j}', 0)) for j in range(1, variable_count + 1)]
        A.append(row)
        B.append(float(data.get(f'd{i}', 0)))
    
    # Convert to numpy arrays
    A = np.array(A)
    B = np.array(B)
    
    # Solve the system
    try:
        solution = np.linalg.solve(A, B)
        return JSONResponse(content={
            "result": {f"x{i+1}": round(float(solution[i]), 2) for i in range(len(solution))}
        })
    except np.linalg.LinAlgError:
        return JSONResponse(content={"error": "System has no solution or infinite solutions"}, status_code=400)

async def polynomial_solver(data):
    try:
        a = float(data.get('a', 0))
        b = float(data.get('b', 0))
        c = float(data.get('c', 0))
        d = float(data.get('d', 0))
        
        equation = CubicEquation([a, b, c, d])
        solution = equation.answers
        
        if not solution:
            return JSONResponse(content={'result': 'No solutions'})
        
        # Create result including both real and imaginary parts if present
        result = {}
        for i, root in enumerate(solution):
            real_part = round(root.real, 4)
            imag_part = round(root.imag, 4)
            
            if abs(imag_part) < 1e-10:  # Check if imaginary part is essentially zero
                result[f'x{i+1}'] = real_part
            else:
                result[f'x{i+1}'] = f'{real_part} + {imag_part}i' if imag_part > 0 else f'{real_part} - {-imag_part}i'

        return JSONResponse(content={'result': result})
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=400)

async def matrix_operations(operation, data):
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
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
        return JSONResponse(content={'error': 'Invalid operation'}, status_code=400)

    return JSONResponse(content={'result': result.tolist() if isinstance(result, np.ndarray) else float(result)}) 