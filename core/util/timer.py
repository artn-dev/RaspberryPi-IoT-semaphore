import time


class Timer:
    def __init__(self, duration):
        self.__duration     = duration
        self.__start_time   = time.time()
        self.__missing_time = 0

    def count(self):
        delta_time = time.time() - self.__start_time
        self.__missing_time = self.__duration - delta_time
        return delta_time >= self.__duration

    def get_missing_time(self):
        return self.__missing_time

