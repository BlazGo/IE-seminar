#!/usr/bin/python
# -*- coding: UTF-8

# PyVisa-Py contains a limited subset of standards.
# PyVisa + NI library required for max support (administrator privileges)

import numpy as np
import time
import random
import pyvisa as pyvisa


class VisVmeter():

    """
    Class for managing voltmeter readings and communication

    Model to use: Keysight DAQ970A
    
    (Optional)
    Model: HP 3456A Digital Voltmeter
    Model: HP 3455A Digital Voltmeter
    """

    def __init__(self, sim = False, meas_num = 10, meas_time = 1):
        """
        Sets up basic instrument parameters.
        Initializes PyVisa
        """

        print("Initializing measuring instrument resources...")

        self.temp = 20
        self.connection = 0
        self.meas_num = meas_num
        self.meas_time = meas_time
        self.sim = sim

        try:
            self.rm = pyvisa.ResourceManager()
            print("Found resources: {}" .format(self.rm.list_resources()))
            # Be careful if connection is not properly closed Visa library can still report device as connected.

        except:
            print("Error with initialization.")

        while self.connection == 0:
            print("Trying to connect...")

            if self.sim == True:
                break

            try:
                self.my_instrument = self.rm.open_resource("USB0::0x2A8D::0x5001::MY58004219::0::INSTR",
                                                            read_termination = "\n", 
                                                            write_termination = "\n")
                response = self.my_instrument.query("?IDN")
                print("Instrument response to ?IDN: {}".format(response))
                
                if response != "ERROR":
                    self.connection = 1

                time.sleep(4)

            except pyvisa.errors.VisaIOError:
                print("----------------------------------------------------")
                print("[ERROR] Problem with instrument. Try to reconfigure.")
                print("----------------------------------------------------")
                time.sleep(5)

            except ValueError:
                print("----------------------------------------------------")
                print("[ERROR] Problem with instrument parameters. Try to reconfigure.")
                print("----------------------------------------------------")
                time.sleep(5)
                pass

        print("Finished initializing measurement instrument resources...")

    def setParameters(self):
        """
        Sets up the instrument parameters
        """

        print("Setting up instrument...")
        self.my_instrument.query_delay = 0.1    # [s] delay after sent command after to continue
        self.my_instrument.timeout = 10000      # [ms] time before timeout error
        
        # Configure a default voltage measurement(range 10V, samples 10, sample time 0.05s, channel 101)
        # self.my_instrument.write("ACQ:VOLT:DC 10, 10, 0.05, (@101)")
                
    def getMeasurement(self):
        """
        Input:
            - "sim" returnes random temp
            - "inst" returns measured temp
        Output:
            - temperature (float)
        """

        print("Getting measurement...")

        try:
            # measure dc voltage, 10V range, 0.001 resolution on channel 101                
            self.my_instrument.query_ascii_values("MEASure:TEMPerature:TCouple? J,0.01,(@105:107)")
        
        except:
            print("WARNING! Error at measurement.")
            self.temp = -1   
            
        return self.temp

    def closeSession(self):
        """
        Properly closes session with the instrument
        (Or else it can still be saved even if device is no tconnected)
        """

        print("Clossing session with instrument...")
        self.rm.close()
        print("Session closed.")


if __name__ == "__main__":
    DAQ = VisVmeter(sim=True)
    DAQ.setParameters()
    print(DAQ.getMeasurement())
    DAQ.closeSession()
    pass


# my_instrument.query("?IDN")
# Same as 
# my_instrument.write("?IDN")
# my_instrument.read()