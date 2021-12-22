from src.utils.Utils import plot_mul_line, check_folder, load_data_yaml
from src.optimal.Search import Search


def run(schemes: list, schemes_num_vehicles: list, step_size: float, epsilon: float, path_log: str, F_R_max=float):
    schemes_average_latency = {key: [] for key in schemes}
    Xs = {key: schemes_num_vehicles for key in schemes}

    for j in schemes_num_vehicles:
        for i in schemes:

            PAPER = Search(option_x=i, num_vehicles=j,
                           step_size=step_size * j, epsilon=epsilon*j, F_R_max=F_R_max)
            total, xs = PAPER.run()

            schemes_average_latency[i].append(total)

    check_folder(f"{path_log}/system_average_latency")
    plot_mul_line(Xs, schemes_average_latency, schemes, "Number vehicles",
                  "System average latency", "System average latency", f"{path_log}/system_average_latency/with_number_vehicles.png")


if __name__ == "__main__":
    CONFIG = load_data_yaml("./src/config/config.yaml")
    run(**CONFIG)
