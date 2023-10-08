from math import cos, sin, fabs, degrees, radians, pi
from game.locator import Locator


class Train:
    def __init__(self,
                 x0: float,
                 y0: float,
                 alpha0: float,
                 v_max: float,
                 locator: Locator,
                 ):
        """метод инициализации класса Train"""

        # координаты мат точки
        self.x = x0
        self.y = y0

        self.alpha = alpha0  # значение угла

        self.locator = locator
        self.v_max = v_max  # максимальная скорость точки

        self.v = 5  # скорость точки

        self.maps = []  # карта обнаружнных препятствий
        self.no_maps = []  # карта точек, в которых не обнаружено ничего

        self.distance = None  # расстояние до препятствия

        self.auto = True  # управление в автоматическом режиме или нет

    def update(self, x: float, y: float):
        """метод обновления информации, приходящей извне"""
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

                self.maps.append(new_point)

        else:
            self.distance = None

    def manual_update(self, x: float, y: float, alpha: float):
        if not self.auto:
            self.x += x
            self.y += y
            self.alpha += alpha

        self.locator.make_query(self.x, self.y, self.alpha)

    def info(self) -> dict:
        """метод отображения текущего состояния"""

        return {
            "params": (self.x, self.y, self.v, self.alpha),
            "maps": self.maps
        }

    def processing(self):
        if self.auto:
            self.processing_auto()

    def processing_auto(self):
        """метод необходимых вычислений"""

        # если есть препятствие
        if self.distance is not None:

            # обновление карты
            if fabs(degrees(self.alpha)) < 90:
                x_new = self.x + self.distance * fabs(cos(self.alpha))
                y_new = self.y + self.distance * fabs(sin(self.alpha))

                if (x_new, y_new) not in self.maps:
                    self.maps.append((x_new, y_new))
            else:
                self.maps.append((self.x + self.distance * cos(self.alpha),
                                  self.y + self.distance * sin(self.alpha)))

            if self.distance == 0:
                self.alpha += radians(100)
                self.alpha %= 2 * pi

                if fabs(degrees(self.alpha)) < 90:
                    self.x = self.x + self.v * fabs(cos(self.alpha))
                    self.y = self.y + self.v * fabs(sin(self.alpha))
                else:
                    self.x = self.x + self.v * cos(self.alpha)
                    self.y = self.y + self.v * sin(self.alpha)

        else:
            # движение точки
            if fabs(degrees(self.alpha)) < 90:
                self.x = self.x + self.v * fabs(cos(self.alpha))
                self.y = self.y + self.v * fabs(sin(self.alpha))
            else:
                self.x = self.x + self.v * cos(self.alpha)
                self.y = self.y + self.v * sin(self.alpha)
