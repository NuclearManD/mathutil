import numpy as np

def mse(a, b):
    return ((a-b)**2).mean(axis=None)
