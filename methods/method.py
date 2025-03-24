from abc import ABC, abstractmethod
from typing import Tuple

from dto.equation import Equation
from dto.result import Result


class Method(ABC):
    """Базовый класс для численных методов решения уравнений"""

    name: str = None  # Название метода (должно быть переопределено)

    def __init__(self, equation: Equation, left: float, right: float,
                 epsilon: float, decimal_places: int, log: bool = False):
        """
        Инициализация численного метода

        Параметры:
        ----------
        equation : Equation
            Объект уравнения с методами function и derivative
        left : float
            Левая граница интервала
        right : float
            Правая граница интервала
        epsilon : float
            Требуемая точность решения
        decimal_places : int
            Количество знаков после запятой для вывода
        log : bool, optional
            Флаг включения логирования (по умолчанию False)

        Исключения:
        -----------
        ValueError
            Если границы интервала некорректны
        """
        if left >= right:
            raise ValueError("Левая граница должна быть меньше правой")

        self.equation = equation
        self.left = left
        self.right = right
        self.epsilon = epsilon
        self.decimal_places = decimal_places
        self.log = log

    @abstractmethod
    def solve(self) -> Result:
        """Абстрактный метод для реализации алгоритма решения"""
        pass

    def check(self) -> Tuple[bool, str]:
        """
        Базовая проверка условий применимости метода

        Возвращает:
        -----------
        tuple(bool, str)
            (Успех, Сообщение об ошибке)
        """
        # Проверка наличия корня через уравнение
        if not self.equation.root_exists(self.left, self.right):
            return False, "На интервале отсутствует корень или их больше одного"

        # Проверка монотонности (если доступна производная)
        try:
            df_left = self.equation.derivative(self.left)
            df_right = self.equation.derivative(self.right)

            if df_left * df_right <= 0:
                return False, "Производная меняет знак на концах интервала"
        except NotImplementedError:
            pass  # Если производная не реализована - пропускаем проверку

        return True, ""

    def _validate_parameters(self):
        """Валидация входных параметров"""
        if self.epsilon <= 0:
            raise ValueError("Точность должна быть положительным числом")
        if self.decimal_places < 0:
            raise ValueError("Количество десятичных знаков не может быть отрицательным")

    def _log_iteration(self, *args, **kwargs):
        """Базовый метод логирования (можно переопределять в дочерних классах)"""
        if self.log:
            print(*args, **kwargs)