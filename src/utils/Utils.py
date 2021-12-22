import random
import matplotlib.pyplot as plt
import os
import yaml


def plot_one_fig_mul_chart(Ys, path_save=""):
    name_plots = list(Ys.keys())
    num_plot = len(name_plots)
    fig, axs = plt.subplots(num_plot)
    fig.set_size_inches(10, 10*num_plot)
    fig.set_dpi(100)
    for i in range(num_plot):
        name_plot = name_plots[i]
        axs[i].plot(range(len(Ys[name_plot])), Ys[name_plot])
        axs[i].set_title(name_plot)
    if path_save:
        plt.savefig(path_save)
    return fig, axs


def plot_mul_line(Xs, Ys, labels, xlabel="", ylabel="", title="", path_save=""):
    fig, axs = plt.subplots(1)
    fig.set_size_inches(15, 10)
    fig.set_dpi(100)
    fig.suptitle(title, fontsize=20)
    for i in labels:
        axs.plot(Xs[i], Ys[i], "o-", label=i)
    axs.set_xlabel(xlabel, fontsize=14)
    axs.set_ylabel(ylabel, fontsize=14)
    leg = axs.legend(loc="upper left", bbox_to_anchor=[0, 1],
                     ncol=2, shadow=True, title="Chú thích", fancybox=True)
    leg.get_title().set_color("red")
    if path_save:
        plt.savefig(path_save)
    return fig, axs


def get_max(values):
    max_value = 0
    index_max = -1
    len_values = len(values)
    for i in range(len_values):
        if values[i] >= max_value:
            max_value = values[i]
            index_max = i
    return max_value, index_max


def get_sum(values, list_choice):
    res = 0
    for i in list_choice:
        res += values[i]
    return res


def check_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def load_data_yaml(path):
    with open(path, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def random_value(value_yaml: dict):
    result = {}
    for key, value in value_yaml.items():
        if value['option'] == 'fix':
            result[key] = value['value']
        elif value['option'] == 'random':
            result[key] = random.randint(
                *value["value"]) if value["type"] == "int" else random.uniform(*value["value"])
    return result
