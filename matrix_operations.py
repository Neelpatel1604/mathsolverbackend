import numpy as np

def add_matrix(matrix1, matrix2):
    try:
        return (np.array(matrix1) + np.array(matrix2)).tolist()
    except ValueError as e:
        raise ValueError(f"Cannot add matrices: {str(e)}")

def subtract_matrix(matrix1, matrix2):
    try:
        return (np.array(matrix1) - np.array(matrix2)).tolist()
    except ValueError as e:
        raise ValueError(f"Cannot subtract matrices: {str(e)}")

def multiply_matrix(matrix1, matrix2):
    try:
        return np.dot(np.array(matrix1), np.array(matrix2)).tolist()
    except ValueError as e:
        raise ValueError(f"Cannot multiply matrices: {str(e)}")

def claculate_determeinant(matrix):
    try:
        return np.linalg.det(np.array(matrix)).tolist()
    except ValueError as e:
        raise ValueError(f"Cannot calculate determinant: {str(e)}")

def invert_matrix(matrix):
    try:
        return np.linalg.inv(np.array(matrix)).tolist()
    except np.linalg.LinAlgError:
        return "Matrix is not invertible"
