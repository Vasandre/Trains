from math import cos, sin, radians, sqrt, tan, degrees, pi
from game.locator import Locator


class Math:
    def __init__(self):
        self.coordinates = []  # список координат
        self.equations = []  # список коээфициентов (k, b) для каждой прямой
        self.intersections = []  # список координат точек пересечения

    def add_list(self, coordinates):
        self.coordinates = coordinates

    def length(self):
        return len(self.coordinates)

    def middle_point(self):
        """
        метод вычисления координат середины отрезка
        :return:
        """

        if self.equations:
            self.equations.clear()

        for number in range(len(self.coordinates) - 1):
            x1, y1 = self.coordinates[number]
            x2, y2 = self.coordinates[number + 1]

            # координаты центра отрезка
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2

            # коэффициент наклона перпендикуляра к прямой
            k = (y2 - y1) / (x2 + x1)

            # коэффициенты уравнения прямой
            k_p = - (1 / k)
            b_p = y_mid - k_p * x_mid

            self.equations.append((k_p, b_p))

    def sums(self) -> tuple:
        """
        метод вычисления сумм по координатам x и y
        :return: суммы по x и y
        """

        length = len(self.equations)

        if self.intersections:
            self.intersections.clear()

        for i in range(length):
            for j in range(i + 1, length):
                k1, b1 = self.equations[i]
                k2, b2 = self.equations[j]

                # координаты пересечения
                x_inter = (b2 - b1) / (k1 - k2)
                y_inter = k1 * x_inter + b1

                self.intersections.append((x_inter, y_inter))

        # суммы по координатам x и y
        x_sum = 0
        y_sum = 0

        for elem in self.intersections:
            x_sum += elem[0]
            y_sum += elem[1]

        return x_sum, y_sum

    def is_circle(self):
        """
         метод аппроксимации данных для получения координат центра и радиуса окружности
        :return: координаты центра окружности (x_c, y_c) и радиус окружности r
        """
        self.middle_point()
        sum_x, sum_y = self.sums()

        len_inter = len(self.intersections)

        # координаты центра окружности
        x_c = sum_x / len_inter
        y_c = sum_y / len_inter

        # список вычисленных радиусов
        radii = []

        for point in self.coordinates:
            x, y = point
            radius = sqrt((x_c - x) ** 2 + (y_c - y) ** 2)
            radii.append(radius)

        # радиус окружности
        r = sum(radii) / len(radii)

        return (x_c, y_c), r

    def approx_circ(self):
        n = len(self.coordinates)
        # сумма по координате x и y
        sum_x = 0
        sum_y = 0

        # сумма квадратов по x и y
        sum_x2 = 0
        sum_y2 = 0

        # сумма кубов по x и y
        sum_x3 = 0
        sum_y3 = 0

        # сумма произведений
        sum_xy = 0
        sum_xy2 = 0
        sum_x2y = 0

        # проход по всем точкам
        for point in self.coordinates:
            x, y = point

            sum_x += x
            sum_y += y

            sum_x2 += x ** 2
            sum_y2 += y ** 2

            sum_x3 += x ** 3
            sum_y3 += y ** 3

            sum_xy += x * y
            sum_xy2 += x * (y ** 2)
            sum_x2y += (x ** 2) * y

        C = n * sum_x2 - sum_x * sum_x
        D = n * sum_xy - sum_x * sum_y
        E = n * sum_x3 + n * sum_xy2 - (sum_x2 + sum_y2) * sum_x
        G = n * sum_y2 - sum_y * sum_y
        H = n * sum_x2y + n * sum_y3 - (sum_x2 + sum_y2) * sum_y

        a = (H * D - E * G) / (C * G - D * D)
        b = (H * C - E * D) / (- (C * G - D * D))
        c = - (a * sum_x + b * sum_y + sum_x2 + sum_y2) / n

        x_c = a / (-2)
        y_c = b / (-2)
        r = sqrt(a ** 2 + b ** 2 - 4 * c) / 2

        return (x_c, y_c), r

    def is_line(self):
        """
        метод аппроксимации данных для получения уравнения прямой
        :return:
        """
        # длина списка
        len_coord = len(self.coordinates)

        # суммы по координатам x и y
        x_sum = 0
        y_sum = 0

        # сумма квадратов x
        x2_sum = 0
        # сумма произведений xy
        xy_sum = 0

        for point in self.coordinates:
            x, y = point
            x_sum += x
            y_sum += y
            x2_sum += x ** 2
            xy_sum += x * y

        k = (len_coord * xy_sum - x_sum * y_sum) / (len_coord * x2_sum - x_sum ** 2)
        b = (y_sum - k * x_sum) / len_coord

        return k, b

    def sort_list(self) -> tuple:
        x_min = min(self.coordinates, key=lambda c: c[0])[0]
        x_max = max(self.coordinates, key=lambda c: c[0])[0]

        diff_x = x_max - x_min

        y_min = min(self.coordinates, key=lambda c: c[1])[1]
        y_max = max(self.coordinates, key=lambda c: c[1])[1]

        diff_y = y_max - y_min

        return diff_x, diff_y


class Objects:
    def __init__(self, name):
        self.name = name

    def area(self):
        pass


class Line(Objects):
    def __init__(self, name, k, b, info):
        super().__init__(name)
        self.k = k
        self.b = b
        self.info = info

    def length(self):
        x1, y1 = self.info[0]
        x2, y2 = self.info[-1]

        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class Circle(Objects):
    def __init__(self, name, x_c, y_c, r, info):
        super().__init__(name)
        self.x_c = x_c
        self.y_c = y_c
        self.r = r
        self.info = info

    def area(self):
        return 2 * pi * self.r


class Train:
    def __init__(self,
                 x0: float,
                 y0: float,
                 alpha0: float,
                 v_max: float,
                 locator: Locator,
                 ):
        """
        метод инициализации класса Train
        :param x0: начальное положение по оси x
        :param y0: начальное положение по оси y
        :param alpha0: начальная ориентация (угол)
        :param v_max: максимальная скорость
        :param locator:
        """

        # координаты материальной точки
        self.x = x0
        self.y = y0

        self.alpha = alpha0  # значение угла

        self.locator = locator
        self.v_max = v_max  # максимальная скорость точки

        self.v = 0  # скорость точки
        print(self.v)

        self.points = []  # список координат обнаруженных точек
        self.math = Math()  # экземпляр класса математики

        # словарь фигур и точек
        self.figures = {
            "lines": [],
            "circles": [],
            "points": self.points
        }

        self.distance = None  # расстояние до препятствия

        self.modes = ["scan", "run", "rotate"]  # список режимов движения
        self.mode = "scan" # режим движения

        self.rotate = 1  # радиан поворота
        self.scan_run = True  # True - сканирование, False - движение
        self.run_rotate = True  # True - движение, False - поворот
        self.count_run = 0

        self.eps = 0.001  # пределе сканирования
        self.count = 1

        self.auto = True  # управление в автоматическом режиме или нет

    def update(self, x: float, y: float):
        """
        метод обновления информации, приходящей извне
        :param x: координата по оси x
        :param y: координата по оси y
        :return:
        """
        if self.auto:
            self.x = x
            self.y = y

        # дергаем измерение локатора
        measurement = self.locator.measurement

        if measurement['query']:
            x_q, y_q, alpha_q = measurement['query'][0]
            self.distance = measurement['distance']

            if self.distance:
                new_point = (
                    x_q + self.distance * cos(alpha_q),
                    y_q + self.distance * sin(alpha_q)
                )

                self.points.append(new_point)

        else:
            self.distance = None

    def manual_update(self, x: float, y: float, alpha: float):
        if not self.auto:
            self.x += x
            self.y += y
            self.alpha += alpha

        self.locator.make_query(self.x, self.y, self.alpha)

    def info(self) -> dict:
        """
        метод отображения текущего состояния
        :return: словарь данных - координаты, скорость, угол и фигуры
        """

        return {
            "params": (self.x, self.y, self.v, self.alpha),
            "maps": self.figures
        }

    def processing(self):
        if self.auto:
            self.processing_auto()

    def processing_auto(self):
        """
        метод необходимых вычислений
        :return:
        """

        print(self.v)
        print("Дистанция", self.distance)
        print("self.mode", self.mode)
        print("self.scan_run", self.scan_run)
        print("self.run_rotate", self.run_rotate)

        # сканирование окружности
        # если есть препятствие
        if self.distance and self.scan_run:
            self.mode = self.modes[0]

        elif self.run_rotate is False:
            self.mode = self.modes[1]

        elif self.run_rotate:
            self.mode = self.modes[2]

        match self.mode:
            case "scan":

                # обновление списка
                self.math.add_list(self.points)

                if self.math.length() > 3:
                    (x_c, y_c), r = self.math.approx_circ()
                    self.figures["circles"] = [((x_c, y_c), r, (0, 25, 255))]

                self.alpha += radians(self.rotate)

                self.run_rotate = True

            case "run":
                self.scan_run = False
                if self.count_run < 36:
                    print(self.v)
                    self.x = self.x + self.v * cos(self.alpha)
                    self.y = self.y + self.v * sin(self.alpha)
                    self.count_run += 1
                    self.run_rotate = False
                else:
                    print("STOP")
                    self.count_run = 0
                    self.run_rotate = True

            case "rotate":
                if self.count == 1:
                    self.alpha += radians(15 - self.rotate)
                    self.count += 1
                    self.mode = self.modes[1]
                    self.run_rotate = False

                elif self.count == 2:
                    self.alpha = self.alpha - radians(90)
                    self.count += 1
                    self.mode = self.modes[1]
                    self.run_rotate = False

                elif self.count == 3:
                    self.alpha -= radians(105)
                    self.count = 1
                    self.mode = self.modes[0]
                    self.run_rotate = True
                    self.scan_run = True

        self.locator.make_query(self.x, self.y, self.alpha)
