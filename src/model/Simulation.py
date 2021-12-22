import math
from os import path
from typing import MutableMapping
from src.model.Vehicle import Vehicle
from src.utils.Utils import get_max, get_sum, random_value, load_data_yaml
from src.model.Optimal import optimal_v, optimal_lamda
import random
import time


class Simulation:
    '''
        Multiple vehicles - one RSU with a VEC server
    '''

    def __init__(self, num_vehicles=10, F_R_max=5*(10**8), option_x="greedy", step_size=0.0000001) -> None:
        self.num_vehicles = num_vehicles
        self.p, self.f, self.f_r, self.v, self.lamda, self.value_tasks, self.x = self.init_optimal_vehicles_variables(
            option_x)
        self.vehicles = self.init_vehicles()
        self.F_R_max = F_R_max
        self.step_size = step_size
        self.list_choice = []
        self.plot_data = {
            "p": [],
            "f": [],
            "f_r": [],
            "lamda": [],
            "v": [],
            "total_latency": []
        }

    def init_vehicles(self):
        vehicles = []
        for i in range(self.num_vehicles):
            vehicles_yaml = load_data_yaml("./src/config/vehicles.yaml")
            vehicle_config = random_value(vehicles_yaml)
            vehicle_config['alpha'] = 1/self.num_vehicles
            vehicles.append(Vehicle(**vehicle_config))
        return vehicles

    def init_optimal_vehicles_variables(self, option_x):
        p, f, f_r, lamda, x, value_tasks, v = [], [], [], [], [], [], 0
        for i in range(self.num_vehicles):
            p.append(random.random())
            f.append(random.random())
            f_r.append(random.random())
            lamda.append(random.random())
            if option_x == "full_vec":
                x.append(1)
            elif option_x == "full_reverse":
                x.append(0)
            else:
                x.append(random.randint(0, 1))
            value_tasks.append(0)
        v = random.random()
        return p, f, f_r, v, lamda, value_tasks, x

    def update_optimal_variable(self):
        for i in range(self.num_vehicles):
            self.p[i] = self.vehicles[i].optimal_transmit_power(
                self.lamda[i])
            self.f[i] = self.vehicles[i].optimal_resource_allocation_vehicle(
                self.x[i], self.lamda[i])
            self.f_r[i] = self.vehicles[i].optimal_resource_allocation_server(
                self.x[i], self.v)
            self.lamda[i] = optimal_lamda(
                lamda=self.lamda[i], vehicle=self.vehicles[i], f=self.f[i], step_size=self.step_size, p=self.p[i])
        self.v = optimal_v(vehicles=self.vehicles,
                           F_R_max=self.F_R_max, xs=self.x)

        self.plot_data['lamda'].append(self.lamda[:])
        self.plot_data['f'].append(self.f[:])
        self.plot_data['f_r'].append(self.f_r[:])
        self.plot_data['p'].append(self.p[:])
        self.plot_data['v'].append(self.v)

    def update_x(self):
        sum_f_r = get_sum(self.f_r, self.list_choice)
        self.value_tasks = [self.vehicles[i].computing_value_task(
            self.f[i], self.x[i]) for i in range(self.num_vehicles)]
        while sum_f_r <= self.F_R_max and (0 in self.x):
            max_value, index_max = get_max(self.value_tasks)
            if index_max >= 0:
                self.list_choice.append(index_max)
                self.x[index_max] = 1
                self.value_tasks[index_max] = -1
                sum_f_r = get_sum(self.f_r, self.list_choice)
            else:
                break
        for i in range(self.num_vehicles):
            if i not in self.list_choice:
                self.x[i] = 0

    def system_average_latency(self):
        Total = 0
        vehicles_latency = []
        for i in range(self.num_vehicles):
            t = self.vehicles[i].total_latency(
                self.p[i], self.f[i], self.f_r[i], self.x[i]) * self.vehicles[i].alpha
            Total += t
            vehicles_latency.append(t)
        self.plot_data['total_latency'].append(vehicles_latency)
        return Total
