import numpy as np

def mse(x: float, y: float) -> float:
    return (x - y )**2



def min_mse(x: float, lst: list[float]) -> float:
    min_error = mse(x, lst[0])
    min_element = lst[0]
    for y in lst[1:]:
        if mse(x, y) < min_error:
            min_error = mse(x, y)
            min_element = y
    return min_element


