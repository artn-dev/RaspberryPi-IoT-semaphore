from threading import Lock
from .util.logger import Logger
from .util.seven_seg import SevenSeg
from .util.movement import MovementDetector
from .util.led import Led


class Facade:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__setup()
        return cls.__instance

    def __setup(self):
        self.__traffic_logger = Logger('logs/traffic.log')
        self.__config_logger  = Logger('logs/config.log')
        self.__car_logger     = Logger('logs/car-count.log')

        self.__traffic_logger_lock = Lock()
        self.__config_logger_lock  = Lock()
        self.__car_logger_lock     = Lock()

        self.__sensor  = MovementDetector()
        self.__display = SevenSeg(16, 18, 15, 13, 11, 12, 10)
        self.__leds = {
                'green':  Led(40),
                'yellow': Led(38),
                'red':    Led(36),
            }

        self.clear_leds()
        self.clear_display()

    def ledon(self, color):
        self.__leds[color].on()

    def ledoff(self, color):
        self.__leds[color].off()

    def clear_leds(self):
        self.__leds['green'].off()
        self.__leds['yellow'].off()
        self.__leds['red'].off()

    def display_number(self, n):
        self.__display.print(n)

    def clear_display(self):
        self.__display.clear()

    def found_movement(self):
        return self.__sensor.found_movement()

    def log_config(self, msg):
        with self.__config_logger_lock:
            self.__config_logger.append(msg)

    def log_traffic(self, msg):
        with self.__traffic_logger_lock:
            self.__traffic_logger.append(msg)

    def log_car(self, color):
        with self.__car_logger_lock:
            log = self.__car_logger.read()
            cars = log.split('\n')

            if color == 'green':
                index = 0
            elif color == 'red':
                index = 1
            else:
                index = 2

            tmp = int(cars[index]) + 1
            cars[index] = str(tmp)
            log = '\n'.join(cars)
            self.__car_logger.write(log, False)

    def read_config(self):
        with self.__config_logger_lock:
            return self.__config_logger.read()

    def read_traffic(self):
        with self.__traffic_logger_lock:
            return self.__traffic_logger.read()

    def read_cars(self):
        with self.__car_logger_lock:
            return self.__car_logger.read()
