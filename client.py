import re
import json
import socket as soc


SERVER_ADDRESS = ('127.0.0.1', 5996)
BUFFER_SIZE    = 4096
OPTIONS        = ['1', '2', 'Q', 'q']


def valid_entry(entry):
    pattern = '|'.join(OPTIONS)
    valid   = re.match(pattern, entry)
    return bool(valid)


def get_new_config():
    data   = {}

    value = int(input('Enter time for green singal: '))
    data['green'] = value

    value = int(input('Enter time for red singal: '))
    data['red'] = value

    value = int(input('Enter time for yellow singal: '))
    data['yellow'] = value

    return data


def get_log():
    while True:
        print('''Which logs do you wish to see?
1. Configuration logs
2. Traffic history
''')
        choice = input('> ')
        
        if choice == '1':
            return 'CONFIG_LOG'

        if choice == '2':
            return 'TRAFFIC_LOG'
        
        print('\nInvalid choice. Please, try again.\n')


try:
    print('Hi there. Hello!')
    username = input('Please enter a username so we can begin: ')

    while True:
        print('''Select what to do:
1. Change the configuration of the semaphore
2. Get the last logs from the semaphore
q. Quit
''')

        choice = input('> ')

        if not valid_entry(choice):
            print('\nInvalid choice. Please, try again.\n')
            continue

        if choice in 'qQ':
            break


        s = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)

        if choice == '1':
            req = { 'command': 'CONFIG', 'user': username }
            req['data'] = get_new_config()

            data = str.encode(json.dumps(req))
            s.sendto(data, SERVER_ADDRESS)

        elif choice == '2':
            req = { 'command': 'LOG', 'user': username }
            req['data'] = get_log()

            data = str.encode(json.dumps(req))
            s.sendto(data, SERVER_ADDRESS)

            data, addr = s.recvfrom(BUFFER_SIZE)
            res = json.loads(data.decode())
            print(res['log'])


except KeyboardInterrupt:
    pass

print('Quitting application.')

