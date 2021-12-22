import math
from mpmath import lambertw


class Vehicle:
    def __init__(self, l_s, l_r, c, beta, d, delta, B, sigma, mu, h_u, h_d, E_max, alpha, p_max, f_max, p_i_RSU) -> None:
        self.l_s = l_s
        self.l_r = l_r
        self.c = c
        self.beta = beta
        self.d = d
        self.delta = delta
        self.B = B
        self.sigma = sigma
        self.h_u = h_u
        self.h_d = h_d
        self.E_max = E_max
        self.mu = mu
        self.alpha = alpha
        self.p_max = p_max
        self.f_max = f_max
        self.p_i_RSU = p_i_RSU

    def uploading_rate(self, p):
        result = p * self.h_u * math.pow(self.d, - self.delta)
        result = result / math.pow(self.sigma, 2)
        # print("uploading_rate", p, result)
        result = math.log2(1 + result)
        return self.B * result

    def downloading_rate(self):
        result = self.p_i_RSU * self.h_d * math.pow(self.d, -self.delta)
        result = result / math.pow(self.sigma, 2)
        # print("downloading_rate", self.p_i_RSU, result)
        result = math.log2(1 + result)
        return self.B * result

    def uploading_latency(self, p):
        return self.l_s / self.uploading_rate(p)

    def reverse_offloading_latency(self):
        return self.beta * self.l_s / self.downloading_rate()

    def vehicle_computation_latency(self, f):
        return self.c * self.beta * self.l_s / f

    def server_computation_latency(self, f_r):
        return self.c * self.l_s / f_r

    def result_download_latency(self):
        return self.l_r / self.downloading_rate()

    def total_latency(self, p, f, f_r, x):
        Total = 0
        if x:
            Total = self.uploading_latency(
                p) + self.server_computation_latency(f_r) + self.result_download_latency()
        else:
            Total = self.uploading_latency(
                p) + self.reverse_offloading_latency() + self.vehicle_computation_latency(f)
        return Total

    def S(self, f,  p):
        S_result = self.uploading_latency(
            p) * p + self.c * self.beta * self.l_s * self.mu * math.pow(f, 2) - self.E_max
        return S_result

    def G(self, f, f_r, x,  p, lamda, v):
        T_total = self.total_latency(p, f, f_r)
        S = self.S(f, p)
        G_result = self.alpha * T_total + lamda * S + v * x * f_r
        return G_result

    def optimal_transmit_power(self, lamda):
        Q = math.log(math.log(2)) + (self.alpha /
                                     lamda + self.p_max) * math.log(2)
        value_check = (Q/(float(lambertw(Q))*math.log(2)) - 1) * \
            math.pow(self.sigma, 2) / self.p_max
        if self.h_u < value_check:
            return self.p_max
        else:
            gamma = self.h_u * \
                math.pow(self.d, - self.delta) / math.pow(self.sigma, 2)
            result = float(lambertw(
                math.exp(-1)*((self.alpha * gamma / lamda) - 1))) + 1
            result = (math.log(2) / result) - 1
            result = math.pow(2, result) / gamma
            return result

    def optimal_resource_allocation_vehicle(self, x, lamda):
        if x == 0:
            result = self.alpha / (2 * lamda * self.mu)
            result = math.pow(result, 1/3)
            result = min(result, self.f_max)
            return result
        else:
            return 0

    def optimal_resource_allocation_server(self, x, v):
        if x == 1:
            result = self.alpha * self.c * self.l_s / v
            result = math.sqrt(result)
            return result
        else:
            return 0

    def computing_value_task(self, f, x):
        if x == 1:
            return -1
        else:
            return self.alpha / (f * self.h_d)
