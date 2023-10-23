from math import cos, sin, radians, sqrt, acos, degrees
from game.locator import Locator


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

    def sort(self, non_sorted):
        min_x = min(non_sorted, key=lambda c: c[0])[0]
        max_x = max(non_sorted, key=lambda c: c[0])[0]
        diff_x = max_x - min_x

        min_y = min(non_sorted, key=lambda c: c[1])[1]
        max_y = max(non_sorted, key=lambda c: c[1])[1]
        diff_y = max_y - min_y

        return diff_x, diff_y

    def angle(self, point1, point2, point3):

        a = (point1[0] - point2[0], point1[1] - point2[1])
        b = (point3[0] - point2[0], point3[1] - point2[1])

        # найдём угол между векторами
        numerator = 0
        temp1 = 0
        temp2 = 0

        for i in range(3):
            numerator += a[i] * b[i]
            temp1 = a[i] ** 2
            temp2 = b[i] ** 2

        corner = acos(numerator / (sqrt(temp1) * sqrt(temp2)))

        return corner

    def processing_auto(self):
        """
        метод необходимых вычислений
        :return:
        """
        self.alpha += radians(2.67466418)

        del_list = []
        # если встречается препятствие на пути
        if self.distance:

            # если ещё нет записи в словаре фигур
            if not self.data:
                # запись будет называться "points"
                self.data["1"] = ["points", None, [self.points[0]]]  # добавление первой точки

            # список существует
            else:
                # проходим по всему списку точек с конца
                for i in range(len(self.points) - 1, -1, -1):
                    point = self.points[i]
                    x_new, y_new = point  # координаты точки
                    flag = False
                    for key in self.data:  # проход по ключам списка

                        flag = False
                        for elem in self.data[key][2]:
                            flag = False

                            # если точки нет в списке
                            if point not in self.data[key][2]:
                                flag = True
                                x, y = elem

                                # вычисление разницы по координате
                                dif_x = abs(x - x_new)
                                dif_y = abs(y - y_new)

                                # если точка попадает в диапазон
                                if (0 <= dif_x <= 30) and (0 <= dif_y <= 30):

                                    # если работаем в поле "points"
                                    if self.data[key][0] == "points":

                                        # добавили точку
                                        self.data[key][2].append(point)

                                        # если длина списка больше двух
                                        if len(self.data[key][2]) > 2:
                                            self.data[key] = self.figure(self.data[key][2])
                                            for el in self.data[key][2]:
                                                del_list.append(self.points.index(el))
                                            break

                                        break

                                    # если работаем с линией
                                    if self.data[key][0] == "line":

                                        # если точка в начале списка
                                        if self.data[key][2].index(elem) == 0:
                                            # вычисление угла
                                            angular = self.angle(point, elem, self.data[key][2][1])
                                            # если угол вне диапазона
                                            if abs(degrees(angular)) >= 120:
                                                self.data[str(len(self.data) + 1)] = ["points", None, [point]]
                                                break
                                            # иначе добавляем в список и сортируем
                                            else:
                                                self.data[key][2].append(point)
                                                dif1, dif2 = self.sort(self.data[key][2])

                                                # если прямая идёт по x
                                                if dif1 > dif2:
                                                    self.data[key][2] = sorted(self.data[key][2], key=lambda d: d[0])
                                                else:
                                                    self.data[key][2] = sorted(self.data[key][2], key=lambda d: d[1])

                                                del_list.append(self.points.index(point))
                                                break

                                        # если точка в конце списка
                                        elif self.data[key][2].index(elem) == len(self.data[key][2]) - 1:

                                            angular = self.angle(point, elem, self.data[key][2][-2])

                                            # если угол вне диапазона
                                            if abs(degrees(angular)) >= 120:
                                                self.data[str(len(self.data) + 1)] = ["points", None, [point]]
                                                break

                                            # иначе добавляем в список и сортируем
                                            else:
                                                self.data[key][2].append(point)
                                                dif1, dif2 = self.sort(self.data[key][2])

                                                # если прямая идёт по x
                                                if dif1 > dif2:
                                                    self.data[key][2] = sorted(self.data[key][2], key=lambda d: d[0])
                                                else:
                                                    self.data[key][2] = sorted(self.data[key][2], key=lambda d: d[1])

                                                del_list.append(self.points.index(point))
                                                break

                                    elif self.data[key][0] == "circle":
                                        # проверяем на причастность к окружности

                                        center, radius = self.data[key][1]
                                        x_c, y_c = center

                                        new_rad = sqrt((x_c - x) ** 2 + (y_c - y) ** 2)

                                        if radius - 10 <= new_rad <= radius + 10:
                                            self.data[key][2].append(point)
                                            self.data[key] = self.is_circ(self.data[key][2])
                                            del_list.append(self.points.index(point))
                                        break

                    # если точка не вошла ни в одну позицию
                    if not flag:
                        self.data[str(len(self.data) + 1)] = ["points", None, [point]]
                        break

            if del_list:
                # удаление из списка точек используемые координаты
                for p in sorted(del_list, reverse=True):
                    del self.points[p]
                del_list.clear()

            # очищаем словарь от окружностей и линий
            self.figures["lines"].clear()
            self.figures["circles"].clear()

            # заполняем словарь значений
            for key in self.data:
                if self.data[key][0] == "line":
                    self.figures["lines"].append(self.data[key][1] + ((0, 25, 255),))
                elif self.data[key][0] == "circle":
                    self.figures["circles"].append(self.data[key][1] + ((0, 25, 255),))

        self.locator.make_query(self.x, self.y, self.alpha)
