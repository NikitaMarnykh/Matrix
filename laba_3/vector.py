from random import uniform


class Vector:
    """Класс, представляющий математический вектор."""

    def __init__(self, size: int = 0, items: tuple | list[int | float] | int | float | None = None) -> None:
        """Инициализирует вектор заданного размера, заполняя его нулями или значениями из списка."""
        self.validated_size(size)
        self.__size: int = size

        if items is None:
            self.__vector: list[int | float] = [0] * size
        else:
            if isinstance(items, (int, float)):
                self.__vector = [items] + [0] * (size - 1)
            elif isinstance(items, (tuple, list)):
                for item in items:
                    self.validated_value(item)
                if len(items) > size:
                    raise ValueError("The number of items exceeds the size of the vector.")
                self.__vector = list(items) + [0] * (size - len(items))
            else:
                raise TypeError("Items can be tuple, list, int, or float.")

    @staticmethod
    def validated_size(size: int) -> None:
        """Проверяет валидность размера вектора."""
        if not isinstance(size, int) or size < 0:
            raise TypeError('The "size" argument must be a positive integer number.')

    def validated_index(self, index: int) -> None:
        """Проверяет валидность индекса."""
        if not isinstance(index, int) or index < 0 or index >= self.__size:
            raise IndexError('The "index" argument must be >= 0 and < size.')

    @staticmethod
    def validated_value(value: int | float) -> None:
        """Проверяет валидность значения."""
        if not isinstance(value, (int, float)):
            raise TypeError('The "value" argument must be either an integer or a float.')

    def validated_vector(self, other: 'Vector') -> None:
        """Проверяет, является ли другой объект вектором и совпадает ли длина с текущим вектором."""
        if not isinstance(other, Vector):
            raise TypeError('The "other" argument is not a vector.')
        if self.__size != other.__size:
            raise ValueError('The vectors must be of the same length.')

    def __add__(self, other: 'Vector') -> 'Vector':
        """Операция сложения двух векторов."""
        self.validated_vector(other)
        return Vector(self.__size, [self.__vector[i] + other.__vector[i] for i in range(self.__size)])

    def __radd__(self, other: 'Vector') -> 'Vector':
        return self + other

    def __iadd__(self, other: 'Vector') -> 'Vector':
        """Операция присваивающего сложения векторов."""
        self.validated_vector(other)
        for i in range(self.__size):
            self.__vector[i] += other.__vector[i]
        return self

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Операция вычитания двух векторов."""
        self.validated_vector(other)
        return Vector(self.__size, [self.__vector[i] - other.__vector[i] for i in range(self.__size)])

    def __rsub__(self, other: 'Vector') -> 'Vector':
        return -self + other

    def __isub__(self, other: 'Vector') -> 'Vector':
        """Операция присваивающего вычитания векторов."""
        self.validated_vector(other)
        for i in range(self.__size):
            self.__vector[i] -= other.__vector[i]
        return self

    def __mul__(self, other: int | float) -> 'Vector':
        self.validated_value(other)
        return Vector(self.__size, [self.__vector[i] * other for i in range(self.__size)])

    def __rmul__(self, other: int | float) -> 'Vector':
        return self * other

    def __imul__(self, other: int | float) -> 'Vector':
        """Операция присваивающего умножения вектора на число."""
        self.validated_value(other)
        for i in range(self.__size):
            self.__vector[i] *= other
        return self

    def __truediv__(self, other: int | float) -> 'Vector':
        """Операция деления вектора на число."""
        self.validated_value(other)
        if other == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return Vector(self.__size, [self[i] / other for i in range(self.__size)])

    def __itruediv__(self, other: int | float) -> 'Vector':
        """Операция присваивающего деления вектора на число."""
        self.validated_value(other)
        if other == 0:
            raise ValueError("Division by zero is not allowed.")
        for i in range(self.__size):
            self.__vector[i] /= other
        return self

    def norma(self) -> float:
        """Вычисляет норму вектора, определяемую максимальным элементом вектора по модулю."""
        return max(abs(v) for v in self.__vector)

    def __str__(self) -> str:
        """Возвращает строковое представление вектора."""
        return f'{self.__vector}'

    def __repr__(self) -> str:
        """Выводит официальное строковое представление вектора."""
        return f'{type(self).__name__}(size={self.__size!r}, elements={self.__vector!r})'

    def __getitem__(self, index: int) -> int | float:
        """Получает элемент вектора по индексу."""
        self.validated_index(index)
        return self.__vector[index]

    def __setitem__(self, index: int, value: int | float) -> None:
        """Устанавливает элемент вектора по индексу."""
        self.validated_index(index)
        self.validated_value(value)
        self.__vector[index] = value

    def __len__(self) -> int:
        """Возвращает размер вектора."""
        return self.__size

    def __neg__(self) -> 'Vector':
        """Возвращает новый вектор, представляющий отрицание текущего."""
        return Vector(self.__size, [-self[i] for i in range(self.__size)])

    @classmethod
    def random_vector(cls, size: int, start: float, end: float) -> 'Vector':
        """Создает случайный вектор заданного размера с элементами в указанном диапазоне."""
        cls.validated_size(size)
        cls.validated_value(start)
        cls.validated_value(end)
        return Vector(size, [round(uniform(start, end), 2) for _ in range(size)])

    @classmethod
    def from_input(cls) -> 'Vector':
        """Создает вектор из пользовательского ввода."""
        size = int(input("Enter the size of the vector: "))
        vector = cls(size)
        print("Enter the vector elements:")
        for i in range(size):
            value = float(input(f"Element {i + 1}: "))
            vector[i] = value
        return vector

    @classmethod
    def write_to_file(cls, file_name: str, vectors: list | tuple) -> None:
        """Записывает список векторов в файл."""
        try:
            with open(file_name, "w") as file:
                for vect in vectors:
                    file.write(f"{' '.join(map(str, vect.__vector))}\n")
        except IOError as e:
            print(f"Error writing to file: {e}")

    @classmethod
    def read_from_file(cls, file_name: str) -> list['Vector']:
        """Читает векторы из файла."""
        vectors = []
        try:
            with open(file_name, "r") as file:
                for line in file:
                    values = list(map(float, line.split()))
                    vect = cls(len(values))
                    for index, value in enumerate(values):
                        vect[index] = value
                    vectors.append(vect)
        except ValueError as e:
            raise ValueError(f"Error reading the file: {e}")
        except IOError as e:
            print(f"Error reading file: {e}")

        return vectors

    def __eq__(self, other) -> bool:
        """Проверяет равенство двух векторов."""
        if not isinstance(other, Vector):
            return False
        return self.__vector == other.__vector

    def __lt__(self, other) -> bool:
        """Проверяет, является ли текущий вектор меньше другого."""
        self.validated_vector(other)
        return self.norma() < other.norma()

    def __le__(self, other) -> bool:
        """Проверяет, является ли текущий вектор меньше или равен другому."""
        self.validated_vector(other)
        return self.norma() <= other.norma()

    def __gt__(self, other) -> bool:
        """Проверяет, является ли текущий вектор больше другого."""
        self.validated_vector(other)
        return self.norma() > other.norma()

    def __ge__(self, other) -> bool:
        """Проверяет, является ли текущий вектор больше или равен другому."""
        self.validated_vector(other)
        return self.norma() >= other.norma()

    def __ne__(self, other) -> bool:
        """Проверяет, является ли текущий вектор неравным другому."""
        return not self == other
