from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from micropython import const
import time;
CONNECTING = 0
CONNECTED = 1

class UARTBLECentralNRF:
    ble = None
    name = ""
    uart = None
    advertisement = None
    #enums for connection status
    #trackin how many time connection has failed
    connectionState = CONNECTING
    connectionFails = 0
    readTimeout = 0.1

    def __init__(self, name):
        self.name = name
        self.ble = BLERadio()
        self.ble.name = self.name
        self.ble.stop_advertising()
        
        self.uart = UARTService()
        self.connectionState = CONNECTING
        self.connectionFails = 0

        self.statusCheckCounter = 0
    
    def timeToChechStatus(self):
        if self.statusCheckCounter > 5:
            self.statusCheckCounter = 0
            return True
        else:
            return False

    def longDisconnected(self):
        return self.connectionFails > 5
    
    def connected(self):
        return self.connectionState == CONNECTED
    
    def evaluate(self):
        if self.connectionState == CONNECTED:
            self.statusCheckCounter += 1
            if self.timeToChechStatus():
                if not self.ble.connected :
                    self.disconnect()
        else:
            #print("evaluate connectiing")
            self.evaluateConnecting()
            return b""
    
    @property
    def in_waiting(self):
        if self.uart is  None:
            return 0
        return self.uart.in_waiting
    
    def evaluateConnecting(self):
        #since this side won't connect to the host, 
        #the central can block
        advertisingTimeUnit = 1.25
        timeout_s = 2
        if self.longDisconnected():
            timeout_s = 1
        if  self.ble.advertising:
            print("already advertising")
            return
        
        
        print("Advertising...")

        #self.uart.deinit()
        #self.uart = UARTService()
        self.advertisement = ProvideServicesAdvertisement(self.uart)
        self.advertisement.short_name = self.name
        self.ble.start_advertising(self.advertisement, interval=advertisingTimeUnit, timeout=timeout_s)
        accumWaitingTime = 0
        
        while (not self.ble.connected) and accumWaitingTime<timeout_s:
            time.sleep(1)
            accumWaitingTime += 1
        print("stop_advertising...")
        
        self.ble.stop_advertising()
        if self.ble.connected:
            self.connectionState = CONNECTED
            self.connectionFails = 0
            print("Split Connected")
            return
        else:
            self.connectionFails += 1
        if self.longDisconnected():
            time.sleep(3)
        else:
            time.sleep(1)
        
        
    def disconnect(self):
        self.connectionState = CONNECTING
        self.connectionFails = 0
        #self.uart  = None

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
        self.evaluate()
        
    def readline(self) -> bytes | None:
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return None
        #connected
        connOK = False
        try:
            s = self.uart.readline()
            connOK = True
        except:
            pass
        return self.evaluate()
    
    def read(self, nbytes: int | None = None ):
        if nbytes is None:
            return None
        if nbytes == 0:
            return None
        if self.connectionState != CONNECTED:
            self.evaluateConnecting()
            return None
        #connected
        retValue = None
        connOK = False
        try:
            retValue = self.uart.read(nbytes)
            connOK = True
        except:
            pass
        self.evaluate()
        return retValue