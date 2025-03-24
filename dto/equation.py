from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import approx_fprime  # Используем актуальный метод для производной


class Equation:
    """
    Класс для представления уравнения и работы с ним.

    Атрибуты:
    - function: Callable - функция уравнения
    - text: str - текстовое описание уравнения
    """

    def __init__(self, function: Callable, text: str):
        self.text = text
        self.function = function

    def draw(self, left: float, right: float, filename: str = 'graph.png') -> None:
        """
        Построение графика функции на заданном интервале.

        Параметры:
        - left: float - левая граница интервала
        - right: float - правая граница интервала
        - filename: str - имя файла для сохранения графика (по умолчанию 'graph.png')
        """
        x = np.linspace(left, right, 1000)
        func = np.vectorize(self.function)(x)

        plt.figure(figsize=(10, 6))
        plt.title(f'График функции: {self.text}')  # Исправлено
        plt.grid(True, which='both', linestyle='--')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(y=0, color='gray', linewidth=0.5, label='y = 0')
        plt.plot(x, func, 'b-', label=self.text)
        plt.legend(loc='best')

        try:
            plt.savefig(filename)
            print(f'График сохранен в {filename}')
        except Exception as e:
            print(f'(!) Ошибка сохранения графика: {str(e)}')

        plt.show()
        plt.close()

    def root_exists(self, left: float, right: float, dx: float = 1e-5) -> bool:
        """
        Проверка существования корня на интервале методом Болцано.
        Учитывает монотонность функции.

        Параметры:
        - left: float - левая граница
        - right: float - правая граница
        - dx: float - шаг для вычисления производной

        Возвращает:
        - bool - True, если есть единственный корень
        """
        try:
            # Проверка смены знака функции
            sign_change = (self.function(left) * self.function(right)) < 0

            # Проверка монотонности через производную в точках
            deriv_left = approx_fprime([left], self.function, dx)[0]
            deriv_right = approx_fprime([right], self.function, dx)[0]

            # Производная сохраняет знак на концах интервала
            monotonic = (deriv_left * deriv_right) > 0

            return sign_change and monotonic
        except Exception as e:
            print(f'(!) Ошибка при проверке корня: {str(e)}')
            return False