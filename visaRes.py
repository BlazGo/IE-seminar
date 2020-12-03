#!/usr/bin/python
# -*- coding: UTF-8

# PyVisa-Py contains a limited subset of standards. PyVisa + NI library required for max support (administrator privileges)
import pyvisa as pyvisa
import random

class VisVmeter():

    """
    Class for managing voltmeter readings and communication

    Model to use: Keysight DAQ970A
    
    (Optional)
    Model: HP 3456A Digital Voltmeter
    Model: HP 3455A Digital Voltmeter

    TODO
    3 measurement instruments
    configuration file to read which instrument to use
    where files are and will be created
    """

    def __init__(self):
        print("Initializing measuring instrument resources...")
    
        self.temp = 20

        print("Finished initializing measurement instrument resources...")

    def setParameters(self):
        print("Setting up instrument...")

    def checkConnection(self):
        print("Checking connection...")

    def getMeasurement(self):
        print("Getting measurement...")

        # calculate random temperature
        self.temp = self.temp + random.randint(-10, 10) / 10
        return self.temp
    
    def restartInstrument(self):
        print("Restarting instrument...")
        print("Finished restarting.")

rm = pyvisa.ResourceManager("@py")
print(rm)
print(rm.list_resources())

# my_instrument = rm.open_resource("GPIB0::8::0::INSTR", read_termination = "\n", write_termination = "\n")
# query_delay = 0.1
# in simulation mode only 8 out of GPIB0 works

# print(my_instrument.query("?IDN"))
# Same as 
# my_instrument.write("?IDN")
# my_instrument.read()

