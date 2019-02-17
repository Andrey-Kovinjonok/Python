import serial.tools.list_ports
from queue import Queue
import time
from threading import Thread

# parser for sms  https://github.com/adammck/pygsm/blob/master/pygsm/message/incoming.py ?
# man http://www.avislab.com/blog/wp-content/uploads/2015/10/Neoway_M590_AT_Command_Sets_V3.0.pdf

writer = Queue()
reader = Queue()

connection = None

def run():
    server_thread = Thread(target=ModemCLI)
    interface_thread = Thread(target=GsmModem)
    server_thread.start()
    interface_thread.start()


class M590Exception(Exception):
    def __init__(self):
        pass


class Sim900Protocol():
    def __init__(self):
        pass


class M590Protocol():
    def __init__(self):
        self.network_name = None
        self.network_status = None
        self.signal_status = None
        self.info_commands = {'modem_ver':b'ATI\r',
                              'module_model': b'AT+CGMM?\r',
                              'firmware_ver': b'AT+GETVERS\r',
                              'status': b'AT + CPAS\r',
                              'network_registration_status': b'AT+CREG?\r',
                              'IMEI': b'AT+CGSN\r',
                              'CIMI': b'AT+CIMI\r',
                              'CCID': b'AT+CCID\r'}
        self.network_service_commands = {'RSSI': b'AT+CSQ'}
        self.sms_commans = {}
        self.special_commands = {'cash_status': b'*100#'} # mean operator commands ..


    def get_cash_status(self):
        pass

    def get_modem_status(self, ser):
        pass

    def get_network_status(self):
        pass

    def get_sim_status(self):
        pass




class ModemCLI():
    def __init__(self):
        print("Start modem CLI interface")
        while not connection:
            pass
        print("interface connected !")
        while connection:
            print ("Enter command:")
            command = input()
            if len(command) > 0:
                command = command+'\r'
                command = command.encode()
                writer.put_nowait(command)
                echo = reader.get(timeout=1)
                print(echo)


class GsmModem(M590Protocol):
    def __init__(self):
        super().__init__()
        print("Start serial server")
        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        print("Connected COM ports: " + str(connected))
        while True:
            global connection
            connection = True
            try:
                with serial.Serial('/dev/ttyUSB0', 9600,
                                   timeout=1) as ser:  # TODO написать процедуру поиска устройства, перебора портов ?
                   while True:
                        line = ser.readline()
                        line = line.decode()
                        if len(line) > 0:
                            reader.put_nowait(line)
                        if not writer.empty() and ser.out_waiting == 0:
                            ser.write(writer.get_nowait())
                        time.sleep(0.01)
            except serial.SerialException as er:
                connection = False
                print("Problem !", er)
                time.sleep(1)
                # print("Cant find device on port ! Try to reconnect")


run()