from typing import Tuple
import decimal

from dto.equation import Equation


def choose_equation_type():
    """
    Предлагает пользователю выбрать тип задачи:
    1 - Нелинейное уравнение, 2 - Система нелинейных уравнений, 3 - Выход.
    Обрабатывает некорректный ввод, запрашивая повторный выбор.
    Возвращает выбранный номер (1, 2 или 3).
    """
    while True:
        print("Выберите тип программы:")
        print('1: Нелинейное уравнение')
        print('2: Система нелинейных уравнений')
        print('3: Выход')

        try:
            equation_type_number = int(input("Введите номер типа: "))
            if equation_type_number in [1, 2, 3]:
                return equation_type_number
            else:
                print("(!) Такого номера нет.")
        except ValueError:
            print('(!) Вы ввели не число')


def choose_equation(functions) -> Equation:
    """
    Предлагает выбрать уравнение из переданного словаря functions,
    где ключ - номер, значение - объект Equation.
    Выводит список уравнений, обрабатывает некорректный ввод.
    Возвращает выбранный объект Equation.
    """
    while True:
        print("Выберите уравнение:")
        for num, func in functions.items():
            print(f"{num}: {func.text}")

        try:
            equation_number = int(input("Введите номер уравнения: "))
            if equation_number in functions:
                return functions[equation_number]
            else:
                print("(!) Такого номера нет.")
        except ValueError:
            print('(!) Вы ввели не число')


def choose_method_number(methods) -> int:
    """
    Предлагает выбрать метод решения из словаря methods,
    где ключ - номер, значение - объект метода с атрибутом name.
    Возвращает выбранный номер метода.
    """
    while True:
        print("Выберите метод:")
        for num, mtd in methods.items():
            print(f"{num}: {mtd.name}")

        try:
            method_number = int(input("Введите номер метода: "))
            if method_number in methods:
                return method_number
            else:
                print("(!) Такого номера нет.")
        except ValueError:
            print('(!) Вы ввели не число')


def print_result(result, output_file_name):
    """
    Выводит результат на экран или в файл.
    Если output_file_name не пустой, записывает результат в файл.
    Иначе выводит в консоль.
    """
    if output_file_name:
        with open(output_file_name, "w") as f:
            f.write(str(result))
        print('Результат записан в файл.')
    else:
        print('\n' + str(result))


def read_initial_data() -> Tuple[float, float, float, int]:
    """
    Считывает начальные данные для задачи с интервалом [a, b]:
    - Левую и правую границы интервала
    - Погрешность вычислений
    Данные можно ввести вручную или загрузить из файла.
    Возвращает кортеж: (left, right, epsilon, decimal_places)
    """
    while True:
        filename = input("Введите имя файла для загрузки данных или пустую строку для ручного ввода: ")
        if filename == '':
            try:
                left = float(input('Введите левую границу интервала: '))
                right = float(input('Введите правую границу интервала: '))
                epsilon = input('Введите погрешность вычисления: ')
                break
            except ValueError:
                print("(!) Введены некорректные числовые значения. Повторите ввод.")
        else:
            try:
                with open(filename, "r") as f:
                    lines = f.read().splitlines()
                    left = float(lines[0])
                    right = float(lines[1])
                    epsilon = lines[2]
                    print(f'Считано из файла: a={left}, b={right}, eps={epsilon}')
                    break
            except (FileNotFoundError, IndexError, ValueError):
                print('(!) Ошибка чтения файла. Проверьте формат и существование файла.')

    # Определение количества десятичных знаков для вывода
    decimal_places = abs(decimal.Decimal(epsilon).as_tuple().exponent)
    epsilon = float(epsilon)
    return left, right, epsilon, decimal_places


def read_initial_data_newton() -> Tuple[float, float, int]:
    """
    Считывает начальные данные для метода Ньютона:
    - Начальное приближение x0
    - Погрешность вычислений
    Поддерживает ручной ввод или загрузку из файла.
    Возвращает кортеж: (x0, epsilon, decimal_places)
    """
    while True:
        filename = input("Введите имя файла для загрузки данных или пустую строку для ручного ввода: ")
        if filename == '':
            try:
                x0 = float(input('Введите начальное приближение: '))
                epsilon = input('Введите погрешность вычисления: ')
                break
            except ValueError:
                print("(!) Некорректный ввод. Введите числовые значения.")
        else:
            try:
                with open(filename, "r") as f:
                    lines = f.read().splitlines()
                    x0 = float(lines[0])
                    epsilon = lines[1]
                    print(f'Считано из файла: x0={x0}, eps={epsilon}')
                    break
            except (FileNotFoundError, IndexError, ValueError):
                print('(!) Ошибка чтения файла. Проверьте формат и существование файла.')

    decimal_places = abs(decimal.Decimal(epsilon).as_tuple().exponent)
    epsilon = float(epsilon)
    return x0, epsilon, decimal_places