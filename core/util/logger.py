from datetime import datetime


class Logger:
    def __init__(self, filepath):
        self._filepath = filepath

    def write(self, msg, timestamp=True):
        with open(self._filepath, 'wt') as log_file:
            if timestamp:
                log_time = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                log_file.write(log_time + ' ')

            log_file.write(msg + '\n')

    def append(self, msg, timestamp=True):
        with open(self._filepath, 'at') as log_file:
            if timestamp:
                log_time = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
                log_file.write(log_time + ' ')

            log_file.write(msg + '\n')

    def read(self):
        txt = None

        with open(self._filepath, 'rt') as log_file:
            txt = log_file.read()

        return txt

