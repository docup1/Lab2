from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def system_a(xy):
    """
    Система уравнений:
    x² + y² - 1 = 0
    x² - y - 0.5 = 0
    """
    x, y = xy
    return [x ** 2 + y ** 2 - 1, x ** 2 - y - 0.5]


def plot_system(system):
    """
    Визуализация системы уравнений:
    Строит контурные графики для каждого уравнения в диапазоне [-2, 2]
    """
    x = np.linspace(-2, 2, 400)
    y = np.linspace(-2, 2, 400)
    X, Y = np.meshgrid(x, y)

    # Вычисление значений уравнений на сетке
    Z1 = np.array([system([x_, y_])[0] for x_, y_ in zip(X.ravel(), Y.ravel())]).reshape(X.shape)
    Z2 = np.array([system([x_, y_])[1] for x_, y_ in zip(X.ravel(), Y.ravel())]).reshape(X.shape)

    plt.figure(figsize=(8, 6))
    plt.contour(X, Y, Z1, levels=[0], colors='r', label='x² + y² = 1')
    plt.contour(X, Y, Z2, levels=[0], colors='b', label='x² - y = 0.5')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()


def solve_system(system, phi1, phi2, x0, epsilon, max_iterations=1000):
    """
    Решение системы методом простой итерации
    :param system: Система уравнений
    :param phi1: Функция для вычисления x_{k+1}
    :param phi2: Функция для вычисления y_{k+1}
    :param x0: Начальное приближение (x, y)
    :param epsilon: Точность
    :param max_iterations: Максимальное число итераций
    :return: Решение, количество итераций
    """
    x = np.array(x0, dtype=float)
    iteration_history = []

    try:
        for i in range(max_iterations):
            x_next = np.array([phi1(x[0], x[1]), phi2(x[0], x[1])])
            error = np.linalg.norm(x_next - x)
            residual = np.abs(system(x_next)).max()  # Максимальная невязка

            iteration_history.append((i, x_next[0], x_next[1], error, residual))

            if error < epsilon and residual < epsilon:
                return x_next, i + 1, iteration_history

            x = x_next

        print(f"Метод не сошелся за {max_iterations} итераций")
        return x, max_iterations, iteration_history
    except Exception as e:
        print(f"Ошибка в процессе итерации: {str(e)}")
        return None, None, iteration_history


def choose_system(systems):
    """
    Интерфейс выбора системы уравнений
    :param systems: Словарь доступных систем
    :return: Выбранная система
    """
    while True:
        print("Доступные системы:")
        for num, (func, desc) in systems.items():
            print(f"{num}: {desc}")

        try:
            choice = int(input("Введите номер системы: "))
            if choice in systems:
                return systems[choice]
            else:
                print("(!) Неверный номер системы")
        except ValueError:
            print("(!) Введите целое число")


def phi1_a(x, y):
    """x = sqrt(1 - y²) для системы A"""
    return np.sqrt(1 - y ** 2)


def phi2_a(x, y):
    """y = x² - 0.5 для системы A"""
    return x ** 2 - 0.5


def run():
    # Словарь доступных систем (функция системы, описание)
    systems = {
        1: (system_a, "x² + y² = 1;  x² - y = 0.5")
    }

    # Выбор системы
    selected_system, system_desc = choose_system(systems)
    print(f"Выбрана система: {system_desc}")

    # Визуализация
    plot_system(selected_system)

    # Ввод начальных данных
    while True:
        try:
            x0, y0 = map(float, input("Начальные приближения (x0 y0 через пробел): ").split())
            epsilon = float(input("Точность (epsilon): "))
            break
        except ValueError:
            print("(!) Некорректный ввод. Введите числа через пробел")

    # Решение
    solution, iterations, history = solve_system(
        selected_system,
        phi1_a,
        phi2_a,
        (x0, y0),
        epsilon
    )

    if solution is not None:
        print("\nРезультат:")
        print(f"x = {solution[0]:.6f}")
        print(f"y = {solution[1]:.6f}")
        print(f"Итераций: {iterations}")
        print(f"Невязки: {selected_system(solution)}")

        # Визуализация сходимости
        its, xs, ys, errors, residuals = zip(*history)
        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.plot(its, xs, label='x')
        plt.plot(its, ys, label='y')
        plt.xlabel('Итерация')
        plt.ylabel('Значение')
        plt.legend()
        plt.title('Сходимость')

        plt.subplot(1, 2, 2)
        plt.plot(its, errors, label='Ошибка')
        plt.plot(its, residuals, label='Невязка')
        plt.yscale('log')
        plt.xlabel('Итерация')
        plt.legend()
        plt.title('Точность')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    run()