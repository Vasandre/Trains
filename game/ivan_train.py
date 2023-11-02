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

    def is_angle(self):
        # берём три точки
        x1, y1 = self.coordinates[-4]
        x2, y2 = self.coordinates[-3]
        x3, y3 = self.coordinates[-2]
        x4, y4 = self.coordinates[-1]

        # вычисяем угол наклона первой прямой
        k1 = (x2 - x1) / (y2 - y1)
        # вычисляем угол наклона второй прямой
        k2 = (x4 - x3) / (y4 - y3)

        # если они противоположны
        if k1 == - 1 / k2:
            return True
        else:
            return False


class Objects:
    def __init__(self):
        pass

    def area(self):
        pass


class Line(Objects):
    def __init__(self, name, k, b, info):
        super().__init__()
        self.name = name
        self.k = k
        self.b = b
        self.info = info

    def length(self):
        """
        метод расчёта длины прямой
        :return:
        """
        x1, y1 = self.info[0]
        x2, y2 = self.info[-1]

        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def coeffs(self):
        """
        метод для вывода коээфициента прямой
        :return:
        """
        return self.k, self.b


class Circle(Objects):
    def __init__(self, name, x_c, y_c, r, info):
        super().__init__()
        self.name = name
        self.x_c = x_c
        self.y_c = y_c
        self.r = r
        self.info = info

    def area(self):
        return 2 * pi * self.r


class Angle(Objects):
    def __init__(self, line1, line2):
        super().__init__()
        self.name = None
        self.x = 0
        self.y = 0
        self.line1 = line1
        self.line2 = line2
        self.type = ""

    def center_point(self):
        """
        метод вычисления координат угла
        :return:
        """
        k1, b1 = self.line1.coeffs()
        k2, b2 = self.line2.coeefs()

        # вычисление координат угла
        self.x = (b2 - b1) / (k1 - k2)
        self.y = k1 * self.x + b1

    def in_or_out(self, my_x, my_y):
        """
        метод определения типа угла: внутренний или наружный
        :param my_x:
        :param my_y:
        :return:
        """
        # крайние точки возле точки угла
        point1 = self.line1.info[-1]
        point2 = self.line2.info[0]

        # расчёт середины отрезка между точками
        x_mid = (point1[0] + point2[0]) / 2
        y_mid = (point1[1] + point2[1]) / 2

        # расчёт расстояния до угла и до середины отрезка
        len1 = sqrt((my_x - x_mid) ** 2 + (my_y - y_mid) ** 2)
        len2 = sqrt((my_x - self.x) ** 2 + (my_y - self.y) ** 2)

        # если от объекта до середины отрезка расстояние больше
        if len1 > len2:
            self.type = "out"
        # иначе
        else:
            self.type = "in"

        return self.type


class Rectangle(Objects):
    def __init__(self, name, angle_points):
        super().__init__()
        self.name = name
        self.angle_points = angle_points
        self.lines_list = []

    def lines(self):
        """
        метод для вывода списка линий
        :return:
        """
        length = len(self.angle_points)

        for i in range(length):
            x1, y1 = self.angle_points[i]
            if i == 3:
                x2, y2 = self.angle_points[0]
            else:
                x2, y2 = self.angle_points[i + 1]

            # добавление 2 точек линии
            self.lines_list.append(((x1, y1), (x2, y2)))

        return self.lines_list


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

        self.points = []  # список координат обнаруженных точек
        self.math = Math()  # экземпляр класса математики

        # словарь фигур и точек
        self.figures = {
            "lines": [],
            "circles": [],
            "points": []
        }

        self.distance = None  # расстояние до препятствия

        self.modes = ["scan", "run", "rotate"]  # список режимов движения
        self.mode = "scan"  # режим движения

        self.rotate = 1  # радиан поворота
        self.scan_run = True  # True - сканирование, False - движение
        self.run_rotate = True  # True - движение, False - поворот
        self.count_run = 0  # сколько прошли
        self.rad = 0  # предыдущее значение угла
        self.dist = 0  # сколько надо пройти

        self.eps = 0.0002  # пределе сканирования
        self.count = 1  # номер поворота

        self.primitives = ""

        self.auto = True  # управление в автоматическом режиме или нет
        self.temp_list = []
        self.angles = []

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
        self.primitives = "borders"

        match self.primitives:
            case "circle":
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

                            if abs(self.rad - r) < self.eps:
                                self.count = 4
                                self.scan_run = False

                            self.rad = r

                            self.figures["circles"] = [((x_c, y_c), r, (0, 25, 255))]
                            self.figures["points"] = [(x_c, y_c)]

                        self.alpha += radians(self.rotate)

                        self.run_rotate = True

                    case "run":

                        if self.dist == 0:
                            self.dist = (self.locator.range() + 100) * abs(cos(radians(15)))
                        self.scan_run = False
                        if self.count_run < self.dist:
                            self.x = self.x + self.v * cos(self.alpha)
                            self.y = self.y + self.v * sin(self.alpha)
                            self.count_run += self.v
                            self.run_rotate = False
                        else:
                            self.count_run = 0
                            self.run_rotate = True
                            if self.count == 2:
                                self.dist = self.dist * tan(radians(15))
                            else:
                                self.dist = 0

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

                        elif self.count == 4:
                            self.x += 0
                            self.y += 0
            case "rectangle":
                pass
            case "borders":

                if self.distance and self.scan_run:

                    # если не посчитана ни одна прямая
                    if not self.temp_list:
                        # если в списке набралось больше 2 точек
                        if len(self.points) > 2:
                            self.math.add_list(self.points)
                            k, b = self.math.is_line()
                            self.temp_list.append(Line("1", k, b, self.points))

                    else:
                        line = self.temp_list[-1]
                        x, y = self.points[-1]

                        a, b = line.coeffs()
                        # если точка принадлежит текущей прямой
                        if y - 5 <= a * x + b <= y + 5:
                            self.math.add_list(self.points)
                            k, b = self.math.is_line()
                            self.temp_list[-1] = Line(str(len(self.temp_list)), k, b, self.points)
                        else:

                            if len(self.points) > 3:
                                del self.points[0:-1]

                            if len(self.points) > 2:
                                self.math.add_list(self.points)
                                k, b = self.math.is_line()
                                self.temp_list.append(Line(str(len(self.temp_list)), k, b, self.points))

                                angle = Angle(self.temp_list[-2], self.temp_list[-1])
                                angle.center_point()
                                angle.in_or_out(self.x, self.y)
                                self.angles.append(angle)
                elif self.distance and self.scan_run is False:
                    if self.distance <= 40:
                        self.alpha += radians(130)
                        self.scan_run = True
                else:
                    if self.dist < 100:
                        self.x = self.x + self.v * cos(self.alpha)
                        self.y = self.y + self.v * sin(self.alpha)
                        self.dist += self.v
                    else:
                        self.dist = 0

                    self.alpha += radians(2)



        self.locator.make_query(self.x, self.y, self.alpha)
