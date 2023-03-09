import random
import time


class MovementDetector:
    def __init__(self, *ports):
        self.count = time.time()

    def found_movement(self):
        found = time.time() - self.count >= 3
        
        if found:
            print('[SENSOR] Found movement')
            self.count = time.time()
        return found

