import numpy as np
from dto.result import Result
from methods.method import Method


class ChordMethod(Method):
    name = 'Метод хорд'

    def check(self):
        """
        Проверяет условия применимости метода:
        1. Наличие корня на интервале [a, b]
        2. Монотонность функции (производная сохраняет знак)
        """
        root_exists, error_message = super().check()
        if not root_exists:
            return False, error_message

        # Дополнительная проверка на достаточное условие сходимости
        try:
            f = self.equation.function
            a, b = self.left, self.right
            df_a = self.equation.derivative(a)
            df_b = self.equation.derivative(b)

            if df_a * df_b <= 0:
                return False, "Производная меняет знак на концах интервала"
        except Exception as e:
            return False, f"Ошибка проверки производной: {str(e)}"

        return True, ""

    def solve(self) -> Result:
        """
        Реализация метода хорд с критериями останова:
        - Достижение максимального числа итераций (10 000)
        - Достижение заданной точности по функции и приближению
        """
        f = self.equation.function
        a, b = self.left, self.right
        epsilon = self.epsilon
        decimal_places = self.decimal_places

        # Инициализация начального приближения
        x_prev = a - f(a) * (b - a) / (f(b) - f(a))
        iteration = 0

        while iteration < 10_000:
            iteration += 1

            # Обновление границ интервала
            if f(a) * f(x_prev) < 0:
                b = x_prev
            else:
                a = x_prev

            # Вычисление нового приближения
            x_curr = a - f(a) * (b - a) / (f(b) - f(a))
            error = abs(x_curr - x_prev)
            residual = abs(f(x_curr))

            if self.log:
                self._log_iteration(iteration, a, b, x_curr, f(a), f(b), error, residual)

            # Критерии останова
            if error <= epsilon and residual <= epsilon:
                break

            x_prev = x_curr
        else:
            print("(!) Метод не сошелся за максимальное число итераций")

        return Result(x_curr, f(x_curr), iteration, decimal_places)

    def _log_iteration(self, it_num: int, a: float, b: float,
                       x: float, fa: float, fb: float,
                       error: float, residual: float) -> None:
        """
        Логирование текущей итерации для отладки
        """
        print(f'Итерация {it_num}:')
        print(f'  a = {a:.5f}, b = {b:.5f}')
        print(f'  x = {x:.5f}')
        print(f'  f(a) = {fa:.2e}, f(b) = {fb:.2e}')
        print(f'  Ошибка: {error:.2e}, Невязка: {residual:.2e}')
        print('-' * 40)