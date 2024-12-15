import unittest
import os
from vector import Vector
from matrix import Matrix


class TestMatrix(unittest.TestCase):

    def setUp(self):
        """Создаем примерные матрицы для тестов."""
        self.matrix_a = Matrix(2, 3)  # Матрица 2x3
        self.matrix_b = Matrix(3, 2)  # Матрица 3x2

        vector = Vector(3, [1, 2, 3])

        self.matrix_a[0] = vector

        vector = Vector(3, [2, 4, 6])
        self.matrix_a[1] = vector

        vector = Vector(2, [1, 2])
        self.matrix_b[0] = vector

        vector = Vector(2, [2, 4])
        self.matrix_b[1] = vector

        vector = Vector(2, [3, 6])
        self.matrix_b[2] = vector

    def test_initialization(self):
        """Тестируем инициализацию матрицы."""
        matrix = Matrix(3, 3)
        self.assertEqual(matrix.__len__(), (3, 3))
        with self.assertRaises(TypeError):
            Matrix(-1, 3)
        with self.assertRaises(TypeError):
            Matrix(2, -2)

    def test_validated_rows_and_cols(self):
        """Тестируем функции проверки количества строк и столбцов."""
        with self.assertRaises(TypeError):
            Matrix.validated_rows(0)
        with self.assertRaises(TypeError):
            Matrix.validated_cols(-1)

    def test_validated_index(self):
        """Тестируем проверки индексации."""
        with self.assertRaises(IndexError):
            self.matrix_a.validated_index(2)
        with self.assertRaises(IndexError):
            self.matrix_a.validated_index((2, 1))
        with self.assertRaises(IndexError):
            self.matrix_a.validated_index((-1, 1))

    def test_validated_value(self):
        """Тестируем проверки значений."""
        with self.assertRaises(TypeError):
            self.matrix_a.validated_value("string")
        with self.assertRaises(ValueError):
            self.matrix_a.validated_value(Vector(2))

    def test_addition(self):
        """Тестируем операцию сложения матриц."""
        matrix_c = self.matrix_a + self.matrix_a
        expected = Matrix(2, 3)
        expected[0] = Vector(3, [2, 4, 6])
        expected[1] = Vector(3, [4, 8, 12])
        self.assertTrue(matrix_c == expected)

    def test_subtraction(self):
        """Тестируем операцию вычитания матриц."""
        matrix_c = self.matrix_a - self.matrix_a
        expected = Matrix(2, 3)
        expected[0] = Vector(3, [0, 0, 0])
        expected[1] = Vector(3, [0, 0, 0])
        self.assertTrue(matrix_c == expected)

    def test_multiplication(self):
        """Тестируем операцию умножения матрицы на вектор."""
        vector = Vector(3, [1, 2, 3])  # Умножаем на вектор
        result_vector = self.matrix_a * vector
        expected_vector = Vector(2, [14, 28])  # Ожидаем: [14, 28]
        self.assertTrue(result_vector == expected_vector)

        # Умножение матриц
        result_matrix = self.matrix_a * self.matrix_b
        expected_matrix = Matrix(2, 2)
        expected_matrix[0] = Vector(2, [14, 28])  # Ожидается: [[14, 28], ...]
        expected_matrix[1] = Vector(2, [28, 56])
        self.assertTrue(result_matrix == expected_matrix)

    def test_division(self):
        """Тестируем операцию деления матрицы на число."""
        matrix_c = self.matrix_a / 2
        expected = Matrix(2, 3)
        expected[0] = Vector(3, [0.5, 1, 1.5])
        expected[1] = Vector(3, [1, 2, 3])
        self.assertTrue(matrix_c == expected)

        with self.assertRaises(ValueError):
            self.matrix_a / 0  # Проверка деления на ноль

    def test_gauss(self):
        """Тестируем метод Гаусса."""
        matrix = Matrix(3, 3)
        matrix[0] = Vector(3, [2, 1, -1])
        matrix[1] = Vector(3, [-3, -1, 2])
        matrix[2] = Vector(3, [-2, 1, 2])
        vector = Vector(3, [8, -11, -3])
        solution = matrix.gauss(vector)
        expected_solution = Vector(3, [2.0, 3.0000000000000004, -0.9999999999999999])
        self.assertEqual(solution, expected_solution)

        with self.assertRaises(ZeroDivisionError):
            singular_matrix = Matrix(2, 2)
            singular_matrix[0] = Vector(2, [1, 2])
            singular_matrix[1] = Vector(2, [2, 4])  # Вырожденная матрица
            singular_matrix.gauss(Vector(2, [5, 10]))

    def test_equivalence(self):
        """Тестируем сравнение матриц."""
        self.assertTrue(self.matrix_a == self.matrix_a)
        self.assertTrue(self.matrix_a != self.matrix_b)

    def test_write_and_read_file(self):
        """Тестируем запись и чтение матрицы из файла."""
        filename = 'test_matrix.txt'
        self.matrix_a.write_to_file(filename)
        loaded_matrix = Matrix.from_file(filename)
        self.assertTrue(self.matrix_a == loaded_matrix)
        os.remove(filename)  # Удалить файл после теста

    def test_random_matrix(self):
        """Тестируем создание случайной матрицы."""
        random_matrix = Matrix.random_matrix(3, 3, 0, 10)
        self.assertEqual(random_matrix.__len__(), (3, 3))

    def test_invalid_file_input(self):
        """Тестируем, что выбрасывается исключение при неправильном вводе файла."""
        with self.assertRaises(FileNotFoundError):
            Matrix.from_file('non_existent_file.txt')

    def tearDown(self) -> None:
        """Очистка файлов после тестов."""
        if os.path.exists('test_matrix.txt'):
            os.remove('test_matrix.txt')


if __name__ == '__main__':
    unittest.main()
