import math
from typing import List
from src.model.Vehicle import Vehicle


def optimal_lamda(lamda, vehicle: Vehicle, step_size, f, p):
    return abs(lamda + step_size * vehicle.S(f, p))


def optimal_v(vehicles: List[Vehicle], F_R_max, xs: list):
    new_v = 0
    for index, vehicle in enumerate(vehicles):
        res = xs[index] * math.sqrt(vehicle.alpha * vehicle.c * vehicle.l_s)
        new_v += res
    new_v = math.pow(new_v / F_R_max, 2)
    return new_v
