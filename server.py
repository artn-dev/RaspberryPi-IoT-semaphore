import json
import socket as soc
import threading as thr
from datetime import datetime
from core.state import *
from core.facade import *


ADDRESS     = ('localhost', 5996)
BUFFER_SIZE = 4096
CARS_LOG_MESSAGE = \
'''==========================
Total of cars crossing on:
 - green: {green}
 - red: {red}
'''


facade = Facade()

s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
s.bind(ADDRESS)


def semaphore():
    state = RedLight(facade)
    while state:
        state = state.handle()


semaphore_thread = thr.Thread(target=semaphore)
semaphore_thread.start()

print('[Server] Initiating')

while True:
    data, addr = s.recvfrom(BUFFER_SIZE)

    if not data:
        continue

    req = data.decode()
    req = json.loads(req)

    if req['command'] == 'CONFIG':
        print('[SERVER] Updating color configurations')
        green  = req['data']['green']
        red    = req['data']['red']
        yellow = req['data']['yellow']

        GreenLight.duration  = green
        RedLight.duration    = red
        YellowLight.duration = yellow

        facade.log_config('Configurations changed to <R:{} G:{} Y{}>'
                          .format(red, green, yellow))

    elif req['command'] == 'LOG':
        print('[SERVER] Responding request for logs')

        if req['data'] == 'CONFIG_LOG':
            res = json.dumps({
                'type': req['data'],
                'log': facade.read_config()
                })

        elif req['data'] == 'TRAFFIC_LOG':
            cars_log = facade.read_cars()
            cars     = cars_log.split('\n')

            log_msg = facade.read_traffic()
            log_msg += CARS_LOG_MESSAGE.format(
                    green=cars[0], red=cars[1])

            res = json.dumps({
                'type': req['data'],
                'log': log_msg
                })

        s.sendto(res.encode(), addr)

print('[SERVER] Shutting down')

