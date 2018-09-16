import socket
import time
import json
ADDR = ("192.168.0.103", 2000)

'''
client = socket.create_connection(ADDR)
cf = client.makefile("r+b", bufsize=0)
cf.write('{"relay1": "off", "relay2": "off", "relay3": "on", "relay4": "on", "relay5": "on", "relay6":"on","relay7":"on","relay8":"on"}')
cf.flush()
values = cf.read(14)
cf.close()
client.close()
print values
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)

# get name
s.sendall('{"get":"name"}')
data = s.recv(1024).split('\x00', 1)[0]
name = json.loads(data)['name']

# get netconfig
s.sendall('{"get":"netconfig"}')
data = s.recv(1024).split('\x00', 1)[0]
netconf = json.loads(data)

# get version
s.sendall('{"get":"version"}')
data = s.recv(1024).split('\x00', 1)[0]
version = json.loads(data)['version']

# get baudrate
s.sendall('{"get":"baudrate"}')
data = s.recv(1024).split('\x00', 1)[0]
baudrate = json.loads(data)['baudrate']

relay_nr = 0
status = 'on'
while True:
    relay_nr += 1
    if relay_nr == 9:
        relay_nr = 1
        if status == 'on':
            status = 'off'
        else:
            status = 'on'
    s.sendall('{"relay%s": "%s"}' % (relay_nr, status))
    data = s.recv(1024).split('\x00', 1)[0]
    json_data = json.loads(data)
    # create final json version
    json_data['relay'] = relay_nr
    json_data['status'] = status
    json_data['name'] = name
    json_data['netconf'] = netconf
    json_data['version'] = version
    json_data['baudrate'] = baudrate
    print json.dumps(json_data, indent=2)
    time.sleep(1)
s.close()
