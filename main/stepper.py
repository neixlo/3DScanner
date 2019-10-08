'''
stepper.py is a class to communicate to a stepper motor via an arduino, driver and a python script from PC USB serial port.
'''

import serial
import io
import time

class stepper():

    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 115200) #check this when no access to arduino is possible
            self.ser.timeout = 1 # time the script waits for the arduino to send something via the serial port
            self.on_flag = 0
            print('')
            print('')
            print('Connection to Arduino established.')            
            print('')        
            print(self.ser) # serial connection information
            print('') 
            print('')
            self.ser.flushInput()
            self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
            self.sio.write("help\n")
            self.sio.flush()
            time.sleep(0.5)
            for i in range(0, 14):        
                print(self.ser.readline())
            print('')
            print('')
        except:
            print("ERROR:\n Initialisation not possible.\n May the Arduino is not connected to serial port '/dev/ttyUSB0' or turned off.")


    def on(self):
        self.ser.flushInput()
        self.sio.write("s2000\n")# set initial speed
        self.sio.write("xon\n")
        self.sio.flush()
        self.on_flag = 1
        print(self.ser.readline()) 
        print(self.ser.readline())

    def off(self):
        self.ser.flushInput()
        self.sio.write("xoff\n")
        self.sio.flush()
        self.on_flag = 0
        print(self.ser.readline())    
        
    def move_to(self, deg):
        if self.on_flag == 0:
            return "Stepper driver is turned off. Run 'self.on()' first to activate the driver."      
        self.ser.flushInput()
        pos = int(deg*17.77)  # 6400÷360=17,77777 based on driver steps/pulses per revision  
        self.sio.write("x%i\n" % pos)
        self.sio.write("mx\n")
        self.sio.flush()
        time.sleep(0.5)
        self.ser.flushInput()
        timeout = time.time() + 25
        while time.time() < timeout:  
            if self.ser.inWaiting() != 0:
                return "moved to %i" % deg
        return "ERROR: timeout of stepper positioning exceeded or stepper not active ('self.on()')"
    
    def set_speed(self, speed):
        if speed in range(1500, 2001):
            s = int(speed) 
            self.sio.write("s%i\n" % s)
            self.sio.flush()
            return "Speed set to %i" % s   
        else:
            return "Set speed as integer between 1500 - 2000."

    def disconnect_serial(self):
        self.ser.close()
        return "Serialport closed."

    def reconnect_serial(self):
        self.ser.open()
        return "Serialport open."

    def reset(self):
        self.off()
        time.sleep(0.5)
        self.disconnect_serial()
        time.sleep(0.5)
        self.reconnect_serial()
        time.sleep(2)
        self.on()
        return "Reset to pos 0 and speed 2000."

