from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
from sympy import sympify, Symbol, sin, cos, tan, sqrt, exp, log
import logging
from cardano_method import CubicEquation
from matrix_operations import add_matrix, subtract_matrix, multiply_matrix, claculate_determeinant, invert_matrix

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Math App!"}

@app.post("/api/evaluate-expression")
async def evaluate_expression(request: Request):
    data = await request.json()
    expression = data.get('expression')
    
    if not expression:
        raise HTTPException(status_code=400, detail="No expression provided")

    try:
        # Clean the expression
        expression = expression.replace('^', '**')
        
        # Create a Symbol for x
        x = Symbol('x')
        
        # Parse the expression
        expr = sympify(expression)
        
        # Generate x values from -10 to 10 with 200 points
        x_vals = np.linspace(-10, 10, 200)
        points = []
        
        # Convert expression to lambda function for faster evaluation
        f = lambda x_val: float(expr.subs(x, x_val))
        
        # Calculate y values and create points
        for x_val in x_vals:
            try:
                y_val = f(x_val)
                # Check if y is a real finite number
                if isinstance(y_val, (int, float)) and np.isfinite(y_val):
                    points.append({'x': float(x_val), 'y': y_val})
            except (ValueError, TypeError, ZeroDivisionError):
                continue
        
        # Get additional information about the expression
        result = {
            'points': points,
            'expression': expression
        }
        
        return result
    
    except Exception as e:
        logging.error(f"Error evaluating expression: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error evaluating expression: {str(e)}")

@app.post("/api/calculate")
async def calculate(request: Request):
    data = await request.json()
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

@app.post("/solve_quadratic")
async def quadratic_solver(request: Request):
    data = await request.json()
    logging.debug(f"Received data for quadratic solver: {data}")
    
    try:
        a = float(data.get('a'))
        b = float(data.get('b'))
        c = float(data.get('c'))
        logging.debug(f"Parsed coefficients: a={a}, b={b}, c={c}")
    except (TypeError, ValueError) as e:
        logging.error(f"Invalid input for quadratic solver: {str(e)}")
        return JSONResponse(content={'error': 'Invalid input. Please provide numeric values for a, b, and c.'}, status_code=400)
    
    if a == 0:
        logging.error("Coefficient 'a' is zero")
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

@app.post("/solve_system")
async def solve_system(request: Request):
    data = await request.json()
    logging.debug(f"Received data for system solver: {data}")
    
    try:
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
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

def solve_polynomial(a, b, c, d):
    equation = CubicEquation([a, b, c, d])
    return equation.answers

@app.post("/solve_polynomial")
async def polynomial_solver(request: Request):
    data = await request.json()
    logging.debug(f"Received data for polynomial solver: {data}")
    
    try:
        a = float(data.get('a'))
        b = float(data.get('b'))
        c = float(data.get('c'))
        d = float(data.get('d'))
        logging.debug(f"Parsed coefficients: a={a}, b={b}, c={c}, d={d}")
    except (TypeError, ValueError) as e:
        logging.error(f"Invalid input for polynomial solver: {str(e)}")
        return JSONResponse(content={'error': 'Invalid input. Please provide numeric values for a, b, c, and d.'}, status_code=400)
    
    try:
        solution = solve_polynomial(a, b, c, d)
        logging.debug(f"Polynomial solution: {solution}")
        
        if solution is None or len(solution) == 0:
            return JSONResponse(content={'result': 'No real solutions'})
        else:
            result = {f'x{i+1}': round(float(x), 4) for i, x in enumerate(solution)}
            return JSONResponse(content={'result': result})
    except Exception as e:
        logging.error(f"Error in polynomial_solver: {str(e)}", exc_info=True)
        return JSONResponse(content={'error': f'Error in solving polynomial equation: {str(e)}'}, status_code=500)

@app.post("/api/matrix/add")
async def add_matrix_route(request: Request):
    data = await request.json()
    logging.debug(f"Received data: {data}")
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
    if not matrix1 or not matrix2:
        return JSONResponse(content={'error': 'Missing matrix parameters'}, status_code=400)
    try:
        result = add_matrix(matrix1, matrix2)
        logging.debug(f"Result: {result}")
        return JSONResponse(content={'result': result})
    except Exception as e:
        logging.error(f"Error in add_matrix: {str(e)}")
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/api/matrix/subtract")
async def subtract_matrix_route(request: Request):
    data = await request.json()
    logging.debug(f"Received data: {data}")
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
    if not matrix1 or not matrix2:
        return JSONResponse(content={'error': 'Missing matrix parameters'}, status_code=400)
    try:
        result = subtract_matrix(matrix1, matrix2)
        logging.debug(f"Result: {result}")
        return JSONResponse(content={'result': result})
    except Exception as e:
        logging.error(f"Error in subtract_matrix: {str(e)}")
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/api/matrix/multiply")
async def multiply_matrix_route(request: Request):
    data = await request.json()
    logging.debug(f"Received data: {data}")
    matrix1 = data.get('matrix1')
    matrix2 = data.get('matrix2')
    
    if not matrix1 or not matrix2:
        return JSONResponse(content={'error': 'Missing matrix parameters'}, status_code=400)
    try:
        result = multiply_matrix(matrix1, matrix2)
        logging.debug(f"Result: {result}")
        return JSONResponse(content={'result': result})
    except Exception as e:
        logging.error(f"Error in multiply_matrix: {str(e)}")
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/api/matrix/determinant")
async def determinant_matrix_route(request: Request):
    data = await request.json()
    logging.debug(f"Received data: {data}")
    matrix = data.get('matrix1')
    
    if not matrix:
        return JSONResponse(content={'error': 'Missing matrix parameter'}, status_code=400)
    try:
        result = claculate_determeinant(matrix)
        logging.debug(f"Result: {result}")
        return JSONResponse(content={'result': result})
    except Exception as e:
        logging.error(f"Error in determinant_matrix: {str(e)}")
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.post("/api/matrix/invert")
async def invert_matrix_route(request: Request):
    data = await request.json()
    logging.debug(f"Received data: {data}")
    matrix = data.get('matrix1')
    
    if not matrix:
        return JSONResponse(content={'error': 'Missing matrix parameter'}, status_code=400)
    try:
        result = invert_matrix(matrix)
        logging.debug(f"Result: {result}")
        return JSONResponse(content={'result': result})
    except Exception as e:
        logging.error(f"Error in invert_matrix: {str(e)}")
        return JSONResponse(content={'error': str(e)}, status_code=500)

@app.route('/api/solve-matrix', methods=['POST'])
async def solve_matrix(request: Request):
    data = await request.json()
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
            return JSONResponse(content={'error': 'Invalid operation'}, status_code=400)

        return JSONResponse(content={'result': result.tolist() if isinstance(result, np.ndarray) else float(result)})
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=400)

@app.get("/test")
async def test_route():
    return JSONResponse(content={"message": "Backend is working"}, status_code=200)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)