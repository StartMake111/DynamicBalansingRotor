import random
import numpy as np
import math
import cmath


# Функция для преобразования из полярных координат в декартовы
def polar_to_cartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def find_phase(values, tachometer):
    tachometer = []
    for i in range(10):
        for i in range(25):
            tachometer.append(1)
        for i in range(25):
            tachometer.append(0)
    # max_val = max(values)
    max_idx = random.randint(150, 300)

    def find_boundaries(data, tachometer, max_idx):
        def find_edge(tachometer, start, step, condition, edge_count):
            count = 0
            current = condition
            for i in range(start, step * len(tachometer), step):
                if current != bool(tachometer[i]):
                    count += 1
                    current = not current
                if count == edge_count:
                    return i
            return None

        if tachometer[max_idx] == 1:
            left = find_edge(tachometer, max_idx - 1, -1, False, 2)
            right = find_edge(tachometer, max_idx, 1, True, 1)
        else:
            left = find_edge(tachometer, max_idx - 1, -1, True, 1)
            print(left)
            right = find_edge(tachometer, max_idx, 1, False, 2)
            print(right)

        return [left, right]

    left, right = find_boundaries(values, tachometer, max_idx)
    phase = (max_idx - left) * 360 / (right - left)
    return phase


def draw_vector_with_phase(phase):
    length = random.uniform(1, 11)

    # Преобразование угла из градусов в радианы
    phase_rad = np.deg2rad(phase)

    # Вычисление координат конца вектора
    x = length * np.cos(phase_rad)
    y = length * np.sin(phase_rad)
    return y, x


def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return (x, y)


def cartesian_to_polar(x, y):

    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return (r, theta)


def polar_to_complex(r, theta):
    z = r * cmath.exp(1j * theta)
    return z


def calculate_U(S, A, index):
    S11, S12, S21, S22 = S[0][0], S[0][1], S[1][0], S[1][1]
    A1, A2 = A[0], A[1]

    if index == 1:
        numerator = (S12 * A1) - (S22 * A2)
        denominator = (S12 / S11) - (S22 / S21)
    elif index == 2:
        numerator = (S21 * A2) - (S11 * A1)
        denominator = (S21 / S22) - (S11 / S21)
    else:
        raise ValueError("Index must be 1 or 2")

    U = [num / denominator for num in numerator]
    return U
