import time
from .util.timer import Timer
from .facade import Facade


class LightState:
    duration = 3

    def __init__(self, color, duration, facade):
        #self._color = color
        self._timer = Timer(duration)
        self._facade = facade

    def handle(self):
        raise NotImplementedError()

    #def get_color(self):
    #    return self._color


class RedLight(LightState):
    def __init__(self, facade):
        super().__init__('red', RedLight.duration, facade)
        print('[STATE] Turn on red LED')
        facade.ledon('red')

    def handle(self):
        if self._facade.found_movement():
            self._facade.log_traffic('Car crossed RED light')
            self._facade.log_car('red')

        if self._timer.count():
            print('[STATE] Turn off red LED')
            self._facade.ledoff('red')
            return GreenLight(self._facade)

        return self


class YellowLight(LightState):
    def __init__(self, facade):
        super().__init__('yellow', YellowLight.duration, facade)
        print('[LED] Turn on yellow LED')
        self._facade.ledon('yellow')

    def handle(self):
        if self._timer.count():
            print('[LED] Turn off yellow LED')
            self._facade.ledoff('yellow')
            return RedLight(self._facade)

        return self


class GreenLight(LightState):
    def __init__(self, facade):
        super().__init__('green', GreenLight.duration, facade)
        print('[LED] Turn on green LED')
        self._facade.ledon('green')

    def handle(self):
        if self._facade.found_movement():
            self._facade.log_traffic('Car crossed GREEN light')
            self._facade.log_car('green')

        if self._timer.count():
            print('[LED] Turn off green LED')
            self._facade.ledoff('green')
            return YellowLight(self._facade)

        return self

