from dto.result import Result
from methods.method import Method


class HalfDivisionMethod(Method):
    name = 'Метод половинного деления'

    def check(self):
        """
        Проверяет условия применимости метода:
        1. Наличие корня на интервале [a, b]
        2. Сохранение знака производной (монотонность)
        """
        # Базовая проверка наличия корня
        root_exists, error_msg = super().check() if hasattr(super(), 'check') else (True, "")

        if not root_exists:
            return False, error_msg

        # Проверка монотонности
        try:
            df_a = self.equation.derivative(self.left)
            df_b = self.equation.derivative(self.right)

            if df_a * df_b <= 0:
                return False, "Производная меняет знак на концах интервала"
        except Exception as e:
            return False, f"Ошибка проверки производной: {str(e)}"

        return True, ""

    def solve(self) -> Result:
        """
        Реализация метода бисекции с критериями останова:
        - Достижение максимальной точности
        - Превышение максимального числа итераций (10 000)
        """
        f = self.equation.function
        a, b = self.left, self.right
        epsilon = self.epsilon
        decimal_places = self.decimal_places
        max_iterations = 10_000

        # Начальная проверка
        fa = f(a)
        fb = f(b)
        if fa * fb >= 0:
            raise ValueError("Нарушены условия теоремы Больцано-Коши")

        for iteration in range(1, max_iterations + 1):
            x = (a + b) / 2
            fx = f(x)
            error = abs(b - a)
            residual = abs(fx)

            # Логирование
            if self.log:
                self._log_iteration(iteration, a, b, x, fa, fb, error, residual)

            # Критерии останова
            if error <= 2 * epsilon and residual <= epsilon:
                break

            # Обновление границ
            if fa * fx < 0:
                b = x
                fb = fx
            else:
                a = x
                fa = fx

        else:
            print("(!) Метод не сошелся за максимальное число итераций")

        return Result(x, fx, iteration, decimal_places)

    def _log_iteration(self, it_num: int, a: float, b: float,
                       x: float, fa: float, fb: float,
                       error: float, residual: float) -> None:
        """
        Структурированное логирование итераций
        """
        print(f"Iter {it_num}:")
        print(f"  a = {a:.6f} | b = {b:.6f}")
        print(f"  x = {x:.6f} | f(x) = {residual:.2e}")
        print(f"  Error: {error:.2e} | Interval: [{a:.3f}, {b:.3f}]")
        print("-" * 40)