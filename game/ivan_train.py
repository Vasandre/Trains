from math import cos, sin, radians, sqrt
from game.locator import Locator
from random import randint


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

        self.pointer = 0  # указатель на первую точку из диапазона
        self.points = []  # список координат обнаруженных точек

        self.data = {}  # словарь фигур

        # словарь фигур и точек
        self.figures = {
            "lines": [],
            "circles": [],
            "points": self.points
        }

        # словарь цветов
        self.color = {
            1: (0, 255, 255),
            2: (127, 255, 212),
            3: (118, 238, 198),
            4: (102, 205, 170),
            5: (69, 139, 116),
            6: (223, 255, 0),
            7: (127, 255, 0),
            8: (118, 238, 0),
            9: (102, 205, 0),
            10: (69, 139, 0)
        }

        self.distance = None  # расстояние до препятствия
        self.rotation = 1  # угол поворота

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

    def is_circ(self, coordinates):
        """
        метод аппроксимации данных для получения координат и радиуса окружности
        :param coordinates: список координат точек
        :return: координаты центра окружности (x_c, y_c) и радиуса окружности r
        """

        equations = []  # список коээфициентов (k, b) для каждой прямой
        for num in range(len(coordinates) - 1):
            # вычисление середины отрезка, соединяющего точки
            x_mid = (coordinates[num][0] + coordinates[num + 1][0]) / 2
            y_mid = (coordinates[num][1] + coordinates[num + 1][1]) / 2

            # вычисление коэффициента наклона прямой
            k = (coordinates[num + 1][1] - coordinates[num][1]) / (coordinates[num + 1][0] - coordinates[num][0])

            # вычисление коээфицтентов (k, b) перпендикулярной прямой
            k_p = - (1 / k)
            b_p = y_mid - k_p * x_mid

            equations.append((k_p, b_p))

        intersections = []  # список координат точек пересечения

        for i in range(len(equations)):
            for j in range(i + 1, len(equations)):
                x_inter = (equations[j][1] - equations[i][1]) / (equations[i][0] - equations[j][0])
                y_inter = equations[i][0] * x_inter + equations[i][1]
                intersections.append((x_inter, y_inter))

        sum_x = 0  # сумма по координате x
        sum_y = 0  # сумма по координате y

        for elem in intersections:
            sum_x += elem[0]
            sum_y += elem[1]

        # вычисление среднего значения точек пересечения
        x_c = sum_x / len(intersections)
        y_c = sum_y / len(intersections)

        # список радиусов
        radius = []

        for el in coordinates:
            radius.append(sqrt((el[0] - x_c) ** 2 + (el[1] - y_c) ** 2))

        # усреднённый радиус окружности
        r = sum(radius) / len(radius)

        return (x_c, y_c), r

    def is_line(self, data):
        """
        метод аппроксимации данных в линию
        :param data: список координат точек
        :return: коэффициент наклона k, параметр b
        """
        n = len(data)
        # суммы по координатам
        x_sum = 0
        y_sum = 0
        # сумма квадратов x
        sum_x2 = 0
        # сумма произведенеий x и y
        sum_xy = 0

        for dat in data:
            x_sum += dat[0]
            y_sum += dat[1]
            sum_x2 += dat[0] ** 2
            sum_xy += dat[0] * dat[1]

        # средние значения по x и y
        mean_x = x_sum / n
        mean_y = y_sum / n

        # разница между координатой и средним значением по координатам
        dif_x = []
        dif_y = []

        for el in data:
            dif_x.append(el[0] - mean_x)
            dif_y.append(el[1] - mean_y)

        # суммы произведений и квадратов
        sum_dif_xy = 0
        sum_dif_x2 = 0

        for i in range(n):
            sum_dif_xy += dif_x[i] * dif_y[i]
            sum_dif_x2 += dif_x[i] ** 2

        k = sum_dif_xy / sum_dif_x2  # коэффициент наклона k
        b = mean_y - k * mean_x  # параметр b

        return k, b

    def figure(self, mas):
        """
        метод определения фигуры
        :param mas: список координат точек
        :return:
        """
        # угловой коэффициент и параметр прямой
        coef, inc = self.is_line(mas)

        temp = []  # временный список

        for point in mas:
            x, y = point
            dist = abs(y - (coef * x + inc))
            temp.append(dist)

        sums = sum([x ** 2 for x in temp])
        variance = sums / (len(mas) - 2)  # расчёт дисперсии

        if -2 < variance < 2:
            k, b = self.is_line(mas)
            point1 = (mas[0][0], k * mas[0][0] + b)
            point2 = (mas[-1][0], k * mas[-1][0] + b)
            return ["line", (point1, point2), mas]
        else:

            return ["circle", (self.is_circ(mas)), mas]

    def processing_auto(self):
        """
        метод необходимых вычислений
        :return:
        """
        self.alpha += radians(2.67466418)

        # если встречается препятствие на пути
        if self.distance:

            # если словарь пуст
            if not self.data:
                # параметров для вычисления должно быть как минимум 2
                if len(self.points) > 2:
                    self.data["1"] = self.figure(self.points.copy())
                    self.points.clear()  # очистка списка

                    # очищаем словарь от окружностей и линий
                    self.figures["lines"].clear()
                    self.figures["circles"].clear()

                    # заполняем словарь значений
                    for key in self.data:
                        if self.data[key][0] == "line":
                            self.figures["lines"].append(self.data[key][1] + ((0, 25, 255),))
                        else:
                            self.figures["circles"].append(self.data[key][1] + ((0, 25, 255),))

            elif self.data and len(self.points) > 2:
                self.data[str(len(self.data) + 1)] = self.figure(self.points.copy())
                self.points.clear()  # очистка списка

            else:

                x_new, y_new = self.points[-1]
                # проходим по всему словарю, а именно по точкам
                for key in self.data:
                    for elem in self.data[key][2]:
                        x, y = elem

                        dif_x = x - x_new
                        dif_y = y - y_new

                        if (0 <= abs(dif_x) < 40) and (0 <= abs(dif_y) < 40):
                            self.data[key][2].append((x_new, y_new))
                            self.data[key] = self.figure(self.data[key][2])
                            self.points.pop()
                            break

                # очищаем словарь от окружностей и линий
                self.figures["lines"].clear()
                self.figures["circles"].clear()

                # заполняем словарь значений
                for key in self.data:
                    if self.data[key][0] == "line":
                        self.figures["lines"].append(self.data[key][1] + ((0, 25, 255),))
                    else:
                        self.figures["circles"].append(self.data[key][1] + ((0, 25, 255),))

        self.locator.make_query(self.x, self.y, self.alpha)
