import sympy as sp
import numpy as np


def parse_matrix(text):
    """Parse matrix from text input. Rows separated by ';' or newlines, elements by ',' or spaces."""
    text = text.strip()
    rows = [r.strip() for r in text.replace(';', '\n').split('\n') if r.strip()]
    data = []
    for row in rows:
        elements = row.replace(',', ' ').split()
        data.append([sp.sympify(e) for e in elements])
    return sp.Matrix(data)


def determinant(matrix):
    return matrix.det()


def inverse(matrix):
    return matrix.inv()


def transpose(matrix):
    return matrix.T


def eigenvalues(matrix):
    return matrix.eigenvals()


def eigenvectors(matrix):
    return matrix.eigenvects()


def matrix_multiply(a, b):
    return a * b


def matrix_add(a, b):
    return a + b


def matrix_subtract(a, b):
    return a - b


def rank(matrix):
    return matrix.rank()


def rref(matrix):
    rref_matrix, pivot_columns = matrix.rref()
    return rref_matrix, pivot_columns
