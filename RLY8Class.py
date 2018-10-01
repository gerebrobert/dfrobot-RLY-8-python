import socket
import json
ADDR = ("192.168.0.103", 2000)


class RLY8:

    def __init__(self, ADDR):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDR)

        # get name
        self.getName()

        # get netconfig
        self.s.sendall('{"get":"netconfig"}')
        self.netconf = self.returnResponseJSON()

        # get version
        self.s.sendall('{"get":"version"}')
        self.version = self.returnResponseJSON()['version']

        # get baudrate
        self.s.sendall('{"get":"baudrate"}')
        self.baudrate = self.returnResponseJSON()['baudrate']

        # get relays' status
        self.getRelayStatus()

    def getName(self):
        self.s.sendall('{"get":"name"}')
        self.name = self.returnResponseJSON()['name']

    def setName(self, name):
        self.s.sendall('{"name":"%s"}' % name)
        if self.verifyResponse():
            self.name = name

    def setBaudrate(self, baudrate):
        self.s.sendall('{"baudrate":"%s"}' % baudrate)
        if self.verifyResponse():
            self.baudrate = baudrate

    def setRelayStatus(self, relaynr, status):
        set = '{"relay%s":"%s"}' % (relaynr, status)
        self.s.sendall(set)
        # must run
        self.returnResponseJSON()
        # reread relay statuses
        self.getRelayStatus()

    def getRelayStatus(self, relaynr=False):
        self.s.sendall('{"get":"relayStatus"}')
        self.status = self.returnResponseJSON()
        # separate relay statuses
        self.relay1 = self.status['relay1']
        self.relay2 = self.status['relay2']
        self.relay3 = self.status['relay3']
        self.relay4 = self.status['relay4']
        self.relay5 = self.status['relay5']
        self.relay6 = self.status['relay6']
        self.relay7 = self.status['relay7']
        self.relay8 = self.status['relay8']

    # verify 'ok', 'error' responses
    def verifyResponse(self):
        if self.returnResponseJSON()['resp'] == 'ok':
            return True
        return False

    # get socket response and jsonify
    def returnResponseJSON(self):
        result = self.s.recv(1024).split('\x00', 1)[0]
        return json.loads(result)
