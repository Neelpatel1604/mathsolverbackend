from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import logging
from math_operations import evaluate_expression, calculate, quadratic_solver, solve_system, polynomial_solver, matrix_operations

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
async def evaluate_expression_route(request: Request):
    data = await request.json()
    return await evaluate_expression(data)

@app.post("/api/calculate")
async def calculate_route(request: Request):
    data = await request.json()
    return await calculate(data)

@app.post("/solve_quadratic")
async def quadratic_solver_route(request: Request):
    data = await request.json()
    return await quadratic_solver(data)

@app.post("/solve_system")
async def solve_system_route(request: Request):
    data = await request.json()
    return await solve_system(data)

@app.post("/solve_polynomial")
async def polynomial_solver_route(request: Request):
    data = await request.json()
    return await polynomial_solver(data)

@app.post("/api/matrix/{operation}")
async def matrix_route(operation: str, request: Request):
    data = await request.json()
    return await matrix_operations(operation, data)

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