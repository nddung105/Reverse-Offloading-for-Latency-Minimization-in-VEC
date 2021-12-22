from src.model.Simulation import Simulation
from src.utils.Utils import plot_one_fig_mul_chart, check_folder
import time


class Search:
    def __init__(self, num_vehicles=20, epsilon=0.000001, option_x="greedy", step_size=0.0000001, path_log="./src/evalution", F_R_max=5*(10**8)) -> None:
        self.num_vehicles = num_vehicles
        self.step_size = step_size
        self.F_R_max = F_R_max
        self.si = Simulation(num_vehicles=self.num_vehicles,
                             option_x=option_x, step_size=self.step_size, F_R_max=self.F_R_max)
        self.option_x = option_x
        self.epsilon = epsilon
        self.path_log = path_log

    def run(self):
        Total_last = 0
        Total = self.epsilon * 100

        print(
            f"- Start | num_vehicles: {self.num_vehicles} | schemes: {self.option_x} |")

        while abs(Total - Total_last) > self.epsilon:
            self.si.update_optimal_variable()
            Total_last = Total
            Total = self.si.system_average_latency()
            if self.option_x == "greedy":
                self.si.update_x()

        print(
            f"- End | system_average_latency: {Total} | X: {self.si.x} |\n\n")

        check_folder(f"{self.path_log}/{self.option_x}")
        plot_one_fig_mul_chart(
            self.si.plot_data, f"{self.path_log}/{self.option_x}/num_vehicles_{self.num_vehicles}_{int(time.time())}.png")

        return Total, self.si.x
