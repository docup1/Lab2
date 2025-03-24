import numpy as np
from scipy.optimize import approx_fprime  # Используем современный метод для производных

from dto.equation import Equation
from dto.result import Result
from methods.method import Method


class SimpleIterationsMethod(Method):
    name = 'Метод простой итерации'

    def __init__(self, equation: Equation, left: float, right: float,
                 epsilon: float, decimal_places: int, log: bool = False):
        """
        Инициализация метода простой итерации

        Параметры:
        ----------
        equation : Equation
            Уравнение для решения
        left : float
            Левая граница интервала
        right : float
            Правая граница интервала
        epsilon : float
            Требуемая точность
        decimal_places : int
            Количество знаков для округления
        log : bool, optional
            Включить логирование (по умолчанию False)

        Исключения:
        -----------
        ValueError
            Неверные параметры или условия сходимости не выполнены
        """
        super().__init__(equation, left, right, epsilon, decimal_places, log)
        self._validate_interval()
        self.phi = self._construct_phi()  # Построение функции итераций

    def _validate_interval(self):
        """Проверка корректности интервала"""
        if self.left >= self.right:
            raise ValueError("Левая граница должна быть меньше правой")

    def _construct_phi(self):
        """Построение функции итераций phi(x)"""
        f = self.equation.function
        # Вычисляем оптимальный коэффициент для lambda
        df_left = approx_fprime([self.left], f, epsilon=1e-6)[0]
        df_right = approx_fprime([self.right], f, epsilon=1e-6)[0]
        max_deriv = max(abs(df_left), abs(df_right))

        # Выбор lambda для обеспечения сходимости
        lmbda = 1 / max_deriv if max_deriv != 0 else 1.0

        # Формируем функцию phi(x) = x - lambda*f(x)
        def phi(x):
            return x - lmbda * f(x)

        return phi

    def check(self) -> tuple[bool, str]:
        """
        Проверка условий сходимости метода:
        1. Наличие корня на интервале
        2. |phi'(x)| < 1 на всем интервале
        """
        # Проверка наличия корня
        if not self.equation.root_exists(self.left, self.right):
            return False, "На интервале отсутствует корень или их несколько"

        # Проверка условия сходимости по производной phi
        x_samples = np.linspace(self.left, self.right, 100)
        for x in x_samples:
            deriv = approx_fprime([x], self.phi, epsilon=1e-6)[0]
            if abs(deriv) >= 1:
                return False, f"Условие |phi'(x)| < 1 не выполнено в точке x={x:.4f}"

        return True, ""

    def solve(self) -> Result:
        """Реализация метода простой итерации"""
        phi = self.phi
        x = (self.left + self.right) / 2  # Начальное приближение - середина интервала
        max_iterations = 1000  # Оптимальный лимит итераций
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            x_prev = x
            x = phi(x)

            # Проверка выхода за границы интервала
            if not (self.left <= x <= self.right):
                raise ValueError(f"Приближение x={x} вышло за границы интервала")

            error = abs(x - x_prev)
            residual = abs(self.equation.function(x))

            # Логирование
            if self.log:
                self._log_iteration(iteration, x_prev, x, error, residual)

            # Критерии останова
            if error <= self.epsilon and residual <= self.epsilon:
                break

        else:
            print("(!) Метод не сошелся за максимальное число итераций")

        return Result(x, self.equation.function(x), iteration, self.decimal_places)

    def _log_iteration(self, it_num: int, x_prev: float, x_curr: float,
                       error: float, residual: float) -> None:
        """Структурированное логирование итераций"""
        print(f"Iter {it_num}:")
        print(f"  x_prev = {x_prev:.6f} | x_curr = {x_curr:.6f}")
        print(f"  Ошибка: {error:.2e} | Невязка: {residual:.2e}")
        print("-" * 40)