from matrix import Matrix
from vector import Vector
from prettytable import PrettyTable


def computational_experiment(matrix: Matrix, exact_solution: Vector) -> float:
    size = matrix.__len__()[0]
    b_vector = Vector(size)

    # Вычисляем вектор правой части b
    for i in range(size):
        b_vector[i] = sum(matrix[i][j] * exact_solution[j] for j in range(size))

    # Решаем полученную систему
    found_solution = matrix.gauss(b_vector)

    # Вычисляем погрешность
    error_vector = exact_solution - found_solution
    error_norm = error_vector.norma()

    return error_norm


def main():
    sizes = [2 ** i for i in range(1, 9)]  # Размеры матриц от 2^1 до 2^7 (2, 4, 8, ..., 256)

    # Создаем объект таблицы
    table = PrettyTable()
    table.field_names = ["Размер системы", "Погрешность"]

    for size in sizes:
        # Генерация случайной обусловленной матрицы
        matrix = Matrix.random_matrix(size, size, 1, 10)

        # Простой способ получить известное решение
        exact_solution = Vector.random_vector(size, 1, 10)

        # Проведение вычислительного эксперимента
        error = computational_experiment(matrix, exact_solution)

        # Добавляем результат в таблицу
        table.add_row([size, f"{error}"])

    # Вывод таблицы
    print(table)


main()