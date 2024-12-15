from vector import Vector
from typing import Union


class Matrix:
    """Класс, представляющий математическую матрицу."""

    def __init__(self, rows: int, cols: int) -> None:
        """Инициализирует матрицу заданного размера, заполняя ее векторами.

        Args:
            rows (int): Количество строк.
            cols (int): Количество столбцов.

        Raises:
            TypeError: Если количество строк или столбцов не является положительным целым числом.
        """
        self.validated_rows(rows)
        self.validated_cols(cols)
        self.__rows: int = rows
        self.__cols: int = cols
        self.__matrix: list[Vector] = [Vector(cols) for _ in range(rows)]

    @staticmethod
    def validated_rows(rows: int) -> None:
        """Проверяет валидность количества строк."""
        if not isinstance(rows, int) or rows <= 0:
            raise TypeError('Rows must be positive integers.')

    @staticmethod
    def validated_cols(cols: int) -> None:
        """Проверяет валидность количества столбцов."""
        if not isinstance(cols, int) or cols <= 0:
            raise TypeError('Cols must be positive integers.')

    def validated_index(self, index: Union[int, tuple[int, int], list[int]]) -> None:
        """Проверяет валидность индекса строки/столбца."""
        if isinstance(index, int):
            if index < 0 or index >= self.__rows:
                raise IndexError('The index of the row must be non-negative and less than the number of rows.')
        elif isinstance(index, (tuple, list)):
            if len(index) != 2 or not all(isinstance(i, int) for i in index):
                raise TypeError('Index must be a tuple or list of two integers.')
            row_index, col_index = index
            if row_index < 0 or row_index >= self.__rows:
                raise IndexError('Row index must be non-negative and less than the number of rows.')
            if col_index < 0 or col_index >= self.__cols:
                raise IndexError('Column index must be non-negative and less than the number of columns.')
        else:
            raise TypeError('Index must be an integer, tuple, or list.')

    def validated_value(self, value: Union[int, float, Vector]) -> None:
        """Проверяет валидность значения."""
        if not isinstance(value, (int, float, Vector)):
            raise TypeError('Value must be an integer, float, or a Vector.')
        if isinstance(value, Vector):
            if len(value) != self.__cols:
                raise ValueError('Vector length must be equal to the number of columns.')

    def __getitem__(self, index: Union[int, tuple[int, int], list[int]]) -> Union[Vector, int, float]:
        """Получает элемент матрицы по индексу."""
        self.validated_index(index)
        if isinstance(index, int):
            return self.__matrix[index]
        if isinstance(index, (tuple, list)):
            row_index, col_index = index
            return self.__matrix[row_index][col_index]

    def __setitem__(self, index: Union[int, tuple[int, int], list[int]], value: Union[Vector, int, float]) -> None:
        """Устанавливает элемент матрицы по индексу."""
        self.validated_index(index)
        self.validated_value(value)

        if isinstance(index, int):
            if not isinstance(value, Vector):
                raise ValueError('Value must be a Vector of length equal to the number of columns.')
            self.__matrix[index] = value
        elif isinstance(index, (tuple, list)):
            row_index, col_index = index
            self.__matrix[row_index][col_index] = value

    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Операция сложения двух матриц."""
        if self.__rows != other.__rows or self.__cols != other.__cols:
            raise ValueError('Matrices must be of the same dimensions for addition.')
        new_matrix = Matrix(self.__rows, self.__cols)
        for i in range(self.__rows):
            new_matrix[i] = self[i] + other[i]
        return new_matrix

    def __radd__(self, other: Union[int, float]) -> 'Matrix':
        """Операция сложения: число + матрица."""
        return self + other

    def __iadd__(self, other: 'Matrix') -> 'Matrix':
        """Присваивающее сложение."""
        if self.__rows != other.__rows or self.__cols != other.__cols:
            raise ValueError('Matrices must be of the same dimensions for addition.')
        for i in range(self.__rows):
            self[i] += other[i]
        return self

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """Операция вычитания двух матриц."""
        if self.__rows != other.__rows or self.__cols != other.__cols:
            raise ValueError('Matrices must be of the same dimensions for subtraction.')
        new_matrix = Matrix(self.__rows, self.__cols)
        for i in range(self.__rows):
            new_matrix[i] = self[i] - other[i]
        return new_matrix

    def __rsub__(self, other: Union[int, float]) -> 'Matrix':
        """Операция вычитания: число - матрица."""
        return -self + other

    def __isub__(self, other: 'Matrix') -> 'Matrix':
        """Присваивающее вычитание."""
        if self.__rows != other.__rows or self.__cols != other.__cols:
            raise ValueError('Matrices must be of the same dimensions for subtraction.')
        for i in range(self.__rows):
            self[i] -= other[i]
        return self

    def __mul__(self, other: Union['Matrix', Vector, int, float]) -> Union['Matrix', Vector]:
        """Операция умножения матрицы на вектор, число или матрицу."""
        if isinstance(other, Matrix):
            if self.__cols != other.__rows:
                raise ValueError(
                    'Number of columns in the first matrix must equal the number of rows in the second matrix.')

            new_matrix = Matrix(self.__rows, other.__cols)
            for i in range(self.__rows):
                for j in range(other.__cols):
                    sum_product = sum(self[i][k] * other[k][j] for k in range(self.__cols))
                    new_matrix[i][j] = sum_product
            return new_matrix

        elif isinstance(other, Vector):
            if self.__cols != len(other):
                raise ValueError('Number of columns in the matrix must equal the size of the vector.')
            result_vector = Vector(self.__rows)
            for i in range(self.__rows):
                sum_product = sum(self[i][j] * other[j] for j in range(self.__cols))
                result_vector[i] = sum_product
            return result_vector

        elif isinstance(other, (int, float)):
            new_matrix = Matrix(self.__rows, self.__cols)
            for i in range(self.__rows):
                new_matrix[i] = self[i] * other
            return new_matrix

        else:
            raise TypeError('Unsupported type for multiplication.')

    def __neg__(self) -> 'Matrix':
        """Оператор отрицания."""
        return -1 * self

    def __truediv__(self, other: Union[int, float, Vector]) -> 'Matrix':
        """Операция деления матрицы на число или вектор."""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Division by zero is not allowed.")
            new_matrix = Matrix(self.__rows, self.__cols)
            for i in range(self.__rows):
                new_matrix[i] = self[i] / other
            return new_matrix

        elif isinstance(other, Vector):
            if self.__cols != len(other):
                raise ValueError('Number of columns in the matrix must equal the size of the vector.')
            new_matrix = Matrix(self.__rows, self.__cols)
            for i in range(self.__rows):
                for j in range(self.__cols):
                    if other[j] == 0:
                        raise ValueError('Division by zero is not allowed in vector division.')
                    new_matrix[i][j] = self[i][j] / other[j]
            return new_matrix

        else:
            raise TypeError('Unsupported type for division.')

    def __len__(self) -> tuple[int, int]:
        """Возвращает размеры матрицы."""
        return self.__rows, self.__cols

    def __str__(self) -> str:
        """Возвращает строковое представление матрицы."""
        return "\n".join(" ".join(str(self[i][j]) for j in range(self.__cols)) for i in range(self.__rows))

    def __repr__(self):
        """Возвращает строковое представление матрицы."""
        return f'{type(self).__name__}(rows={self.__rows}, cols={self.__cols})'

    def __eq__(self, other: 'Matrix') -> bool:
        """Сравнение на равенство."""
        if self.__rows != other.__rows or self.__cols != other.__cols:
            return False
        return all(self[i] == other[i] for i in range(self.__rows))

    def __ne__(self, other: 'Matrix') -> bool:
        """Сравнение на неравенство."""
        return not self == other

    def __lt__(self, other: 'Matrix') -> bool:
        """Сравнение на меньше."""
        return self.sum_elements() < other.sum_elements()

    def __le__(self, other: 'Matrix') -> bool:
        """Сравнение на меньше или равно."""
        return self.sum_elements() <= other.sum_elements()

    def __gt__(self, other: 'Matrix') -> bool:
        """Сравнение на больше."""
        return self.sum_elements() > other.sum_elements()

    def __ge__(self, other: 'Matrix') -> bool:
        """Сравнение на больше или равно."""
        return self.sum_elements() >= other.sum_elements()

    def sum_elements(self) -> float:
        """Суммирует все элементы матрицы."""
        return sum(self[i][j] for i in range(self.__rows) for j in range(self.__cols))

    @classmethod
    def random_matrix(cls, rows: int, cols: int, start: Union[int, float], end: Union[int, float]) -> 'Matrix':
        """Создает случайную матрицу заданного размера с элементами в указанном диапазоне.

        Args:
            rows (int): Количество строк.
            cols (int): Количество столбцов.
            start (int | float): Начало диапазона значений.
            end (int | float): Конец диапазона значений.

        Returns:
            Matrix: Новая матрица с случайными элементами.
        """
        cls.validated_rows(rows)
        cls.validated_cols(cols)
        new_matrix = cls(rows, cols)
        for i in range(rows):
            new_matrix[i] = Vector.random_vector(cols, start, end)
        return new_matrix

    @classmethod
    def from_input(cls) -> 'Matrix':
        """Создает матрицу из пользовательского ввода.

        Returns:
            Matrix: Новая матрица, созданная из пользовательского ввода.
        """
        rows = int(input("Enter the number of rows: "))
        cols = int(input("Enter the number of columns: "))
        matrix = cls(rows, cols)
        print("Enter the matrix elements (row by row):")
        for row in range(rows):
            row_elements = list(map(float, input().split()))
            if len(row_elements) != cols:
                raise ValueError(f'The number of elements in the row {row + 1} must be equal to {cols}.')
            matrix[row] = Vector(cols)
            for col in range(cols):
                matrix[row][col] = row_elements[col]

        return matrix

    def write_to_file(self, filename: str) -> None:
        """Записывает матрицу в файл.

        Args:
            filename (str): Имя файла, в который нужно записать матрицу.
        """
        with open(filename, 'w') as f:
            for row in self.__matrix:
                f.write(' '.join(str(value) for value in row) + '\n')

    @classmethod
    def from_file(cls, filename: str) -> 'Matrix':
        """Читает матрицу из файла.

        Args:
            filename (str): Имя файла для чтения.

        Returns:
            Matrix: Новая матрица, считанная из файла.

        Raises:
            ValueError: Если возникает ошибка при чтении файла.
        """
        with open(filename, 'r') as f:
            rows = 0
            cols = 0
            matrix_data = []

            for line in f:
                row = list(map(float, line.split()))
                if cols == 0:
                    cols = len(row)
                elif cols != len(row):
                    raise ValueError(f'The number of elements in the row {rows + 1} does not match the previous rows.')
                matrix_data.append(row)
                rows += 1

            matrix = cls(rows, cols)
            for row in range(rows):
                matrix[row] = Vector(cols)
                for col in range(cols):
                    matrix[row][col] = matrix_data[row][col]

            return matrix

    def gauss(self, col_of_free_mem: Vector) -> Vector:
        """Решает систему линейных уравнений методом Гаусса с помощью единственного деления.

        Args:
            col_of_free_mem (Vector): Вектор свободных членов.

        Returns:
            Vector: Вектор решений системы.

        Raises:
            ValueError: Если система уравнений несовместна или неопределена.
            ZeroDivisionError: Если обнаружена вырожденная матрица.
        """
        # Проверяем, что матрица квадратная и вектор свободных членов имеет нужный размер
        if self.__rows != self.__cols:
            raise ValueError('The matrix must be square (n x n) for the Gauss method.')
        if self.__rows != col_of_free_mem.__len__():
            raise ValueError(
                "The length of the column of free terms must be equal to the number of rows in the matrix.")

        # Формируем расширенную матрицу
        extended_matrix: 'Matrix' = Matrix(self.__rows, self.__cols + 1)

        for row in range(self.__rows):
            for col in range(self.__cols):
                extended_matrix[row][col] = self[row][col]
            extended_matrix[row][self.__cols] = col_of_free_mem[row]

        # Прямой ход с выбором ведущего элемента
        for i in range(self.__rows):
            # Поиск строки с максимальным по модулю элементом в текущем столбце
            max_row = i + max(range(self.__rows - i), key=lambda r: abs(extended_matrix[i + r][i]))
            extended_matrix[i], extended_matrix[max_row] = extended_matrix[max_row], extended_matrix[i]

            # Проверка на вырожденность: если ведущий элемент равен нулю после перестановки
            if abs(extended_matrix[i][i]) < 1e-12:  # Пороговое значение для определения нуля
                raise ZeroDivisionError(
                    f"System of equations is inconsistent or underdetermined (leading element = 0) in row {i + 1}.")

            # Обнуление под ведущим элементом
            for j in range(i + 1, self.__rows):
                factor = extended_matrix[j][i] / extended_matrix[i][i]
                for k in range(i, self.__cols + 1):
                    extended_matrix[j][k] -= factor * extended_matrix[i][k]

        # Обратный ход для нахождения решения
        solution: 'Vector' = Vector(self.__rows)
        for i in range(self.__rows - 1, -1, -1):
            sum_ax = sum(extended_matrix[i][j] * solution[j] for j in range(i + 1, self.__rows))
            solution[i] = (extended_matrix[i][self.__cols] - sum_ax) / extended_matrix[i][i]

        return solution
