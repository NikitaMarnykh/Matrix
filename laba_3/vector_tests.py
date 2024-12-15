import unittest
import os
from vector import Vector


class TestVector(unittest.TestCase):

    def setUp(self):
        """Создание примеров векторов для тестов."""
        self.vector_a = Vector(3, [1, 2, 3])
        self.vector_b = Vector(3, [4, 5, 6])
        self.vector_c = Vector(3, [1, 2, 3])

    def test_addition(self):
        """Проверка сложения двух векторов."""
        result = self.vector_a + self.vector_b
        expected = Vector(3, [5, 7, 9])
        self.assertEqual(result, expected)

    def test_subtraction(self):
        """Проверка вычитания двух векторов."""
        result = self.vector_a - self.vector_b
        expected = Vector(3, [-3, -3, -3])
        self.assertEqual(result, expected)

    def test_multiplication(self):
        """Проверка умножения вектора на число."""
        expected1 = Vector(3, [2, 4, 6])
        test_vector = self.vector_a * 2
        self.assertEqual(test_vector, expected1)

        test_vector = 2 * self.vector_a
        self.assertEqual(test_vector, expected1)

        test_vector = Vector(3, [1, 2, 3])
        test_vector *= 2
        self.assertEqual(test_vector, expected1)

    def test_division_by_scalar(self):
        """Проверка деления вектора на число."""
        result = self.vector_a / 2
        expected = Vector(3, [0.5, 1.0, 1.5])
        self.assertEqual(result, expected)

    def test_norma(self):
        """Проверка вычисления нормы вектора."""
        self.assertEqual(self.vector_a.norma(), 3)

    def test_exceptions(self):
        """Проверка обработки исключений."""
        with self.assertRaises(ValueError):
            self.vector_a + Vector(4)  # разные размеры

        with self.assertRaises(IndexError):
            var = self.vector_a[3]  # выход за пределы

        with self.assertRaises(TypeError):
            self.vector_a[0] = "string"  # не число

        with self.assertRaises(ZeroDivisionError):
            self.vector_a / 0  # деление на ноль

    def test_random_vector(self):
        """Проверка создания случайного вектора."""
        random_vector = Vector.random_vector(3, 1, 10)
        self.assertEqual(len(random_vector), 3)
        self.assertTrue(all(1 <= value <= 10 for value in random_vector))

    def test_file_read_write(self):
        """Проверка записи и чтения векторов из файла."""
        filename = 'test_vectors.txt'
        Vector.write_to_file(filename, [self.vector_a, self.vector_b])

        vectors = Vector.read_from_file(filename)
        self.assertEqual(len(vectors), 2)
        self.assertTrue(vectors[0] == self.vector_a)
        self.assertTrue(vectors[1] == self.vector_b)

        # Удаление файла после теста
        if os.path.exists(filename):
            os.remove(filename)

    def test_len(self):
        """Проверка метода __len__()"""
        self.assertEqual(len(self.vector_a), 3)

    def test_neg(self):
        """Проверка метода __neg__()"""
        result = -self.vector_a
        expected = Vector(3, [-1, -2, -3])
        self.assertEqual(result, expected)

    def test_setitem(self):
        """Проверка метода __setitem__()"""
        self.vector_a[0] = 10
        self.assertEqual(self.vector_a[0], 10)

    def test_getitem(self):
        """Проверка метода __getitem__()"""
        self.assertEqual(self.vector_a[1], 2)

    def test_comparison(self):
        """Проверка операторов сравнения между векторами."""
        self.assertTrue(self.vector_a == self.vector_c)  # равенство
        self.assertFalse(self.vector_a == self.vector_b)  # не равенство
        self.assertTrue(self.vector_a < self.vector_b)  # меньше
        self.assertTrue(self.vector_a <= self.vector_c)  # меньше или равно
        self.assertTrue(self.vector_b > self.vector_a)  # больше
        self.assertTrue(self.vector_b >= self.vector_c)  # больше или равно
