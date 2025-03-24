import numpy as np
from scipy.optimize import approx_fprime  # Используем современную функцию для производной
from dto.result import Result
from methods.method import Method


class NewtonMethod(Method):
    name = 'Метод Ньютона'

    def __init__(self, equation, x0, epsilon, decimal_places, log=False, max_iterations=1000):
        """
        Инициализация метода Ньютона.

        Параметры:
        equation : Equation
            Уравнение для решения, должен иметь методы function и derivative
        x0 : float
            Начальное приближение
        epsilon : float
            Требуемая точность
        decimal_places : int
            Количество знаков после запятой в результате
        log : bool, optional
            Включить вывод лога каждой итерации
        max_iterations : int, optional
            Максимальное количество итераций (по умолчанию 1000)
        """
        super().__init__(equation, x0, x0, epsilon, decimal_places, log)
        self.x0 = x0
        self.max_iterations = max_iterations
        self._validate_initial_conditions()

    def _validate_initial_conditions(self):
        """Проверка начальных условий для метода Ньютона"""
        # Проверка, что производная в начальной точке не равна нулю
        df = self.equation.derivative(self.x0)
        if np.isclose(df, 0.0, atol=1e-6):
            raise ValueError("Производная в начальной точке близка к нулю")

    def check(self):
        """Проверка условий сходимости метода Ньютона"""
        # Проверка наличия корня в окрестности (не строгая, так как метод может сойтись издалека)
        # Основная проверка - ненулевая производная в начальной точке
        try:
            df = self.equation.derivative(self.x0)
            if abs(df) < 1e-6:
                return False, "Производная в начальной точке слишком мала"
        except Exception as e:
            return False, f"Ошибка при вычислении производной: {e}"

        return True, ""

    def solve(self) -> Result:
        """Реализация метода Ньютона"""
        f = self.equation.function
        x = self.x0
        iteration = 0
        dx = np.sqrt(self.epsilon)  # Оптимальный шаг для численной производной

        while iteration < self.max_iterations:
            iteration += 1

            # Вычисляем производную в текущей точке
            df = approx_fprime([x], f, epsilon=dx)[0]

            # Проверка деления на ноль
            if np.isclose(df, 0.0, atol=1e-15):
                raise ValueError(f"Производная близка к нулю на итерации {iteration}")

            x_prev = x
            x = x_prev - f(x_prev) / df  # Формула Ньютона

            # Вычисляем ошибки
            error = abs(x - x_prev)
            residual = abs(f(x))

            # Логирование
            if self.log:
                self._log_iteration(iteration, x_prev, x, df, error, residual)

            # Проверка критериев останова
            if error <= self.epsilon and residual <= self.epsilon:
                break

        else:
            print("(!) Метод не сошелся за максимальное число итераций")

        return Result(x, f(x), iteration, self.decimal_places)

    def _log_iteration(self, it_num, x_prev, x_curr, deriv, error, residual):
        """Логирование одной итерации"""
        print(f"Iter {it_num}:")
        print(f"  Предыдущее приближение: {x_prev:.6f}")
        print(f"  Текущее приближение: {x_curr:.6f}")
        print(f"  Производная: {deriv:.2e}")
        print(f"  Изменение x: {error:.2e}")
        print(f"  Невязка: {residual:.2e}")
        print("-" * 40)