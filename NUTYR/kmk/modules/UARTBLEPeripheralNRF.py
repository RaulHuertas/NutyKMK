from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from micropython import const
import time;
CONNECTING = 0
CONNECTED = 1

class UARTBLEPeripheralNRF:
    ble = None
    name = ""
    uart = None
    connectionFails = 0
    readTimeout = 0.1

    def __init__(self, name):
        self.name = name
        self.ble = BLERadio()
        self.connectionState = CONNECTING
        self.connectionFails = 0

    def longDisconnected(self):
        return self.connectionFails > 5
    
    def connected(self):
        return self.connectionState == CONNECTED
    
    def evaluate(self):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()

    def evaluateConnecting(self):
        #since this side won't connect to the host, 
        #the central can block
        devicesFound =  self.ble.start_scan(ProvideServicesAdvertisement,timeout = 0.5)
        for adv in devicesFound:
            print((adv))
            print((adv.short_name))
            if adv.short_name != self.name:
                continue;
            if UARTService in adv.services:
                print("expected device found!") 
                self.uart = self.ble.connect(adv)
                self.uart = self.uart[UARTService]
                self.connectionState = CONNECTED
                self.connectionFails = 0
                print("Connected")
                break
    
        if not self.connected():
            self.connectionFails += 1
        
        self.ble.stop_scan()
        time.sleep(3)
        

    def write(self,buf: circuitpython_typing.ReadableBuffer):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return

        #connected
        connOK = False
        try:
            self.uart.write(buf)
            connOK = True
        except:
            pass
        if not connOK or not self.ble.connected:
            self.connectionState = CONNECTING

    def readline(self) -> bytes | None:
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            print("x1")
            return None
        #connected
       # print("x2")
        s = None
        try:
            s = self.uart.readline()
            #print("x3")
        except:
            #print("x4")
            pass
        if not self.ble.connected :
            self.connectionState = CONNECTING
            print("x5")
        
        #print("x6")
        return s
    
    def read(self, nbytes: int | None = None ):
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return
        #connected
        retValue = None
        try:
            retValue = self.uart.read(nbytes)
        except:
            pass
        if  not self.ble.connected:
            self.connectionState = CONNECTING

        return retValue
         