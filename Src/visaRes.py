#!/usr/bin/python
# -*- coding: UTF-8

# PyVisa-Py contains a limited subset of standards.
# PyVisa + NI library required for max support (administrator privileges)

import numpy as np
import time
import random
import pyvisa as pyvisa
from datetime import datetime


class pyVisDAQ():
    """ Instrument control class
    Usage:
        - connects with the instrument
        - get measurement
        - close session
        - set measurement and instrument parameters
    """

    def __init__(self, sim=False, meas_num=10, meas_time=1):
        """ Initialization
        Sets up a connection with the instrument
        """

        self.start_time = datetime.now()
        print("\n---------------------------------------------------")
        print("Start time: {}\n".format(self.start_time.strftime("%Y/%m/%d %H:%M:%S")))
        print("Initializing instrument resources...")

        self.sim = sim
        self.meas_num = meas_num    # [/] number of measurements in time frame
        self.meas_time = meas_time  # [s] time for all measurements
        connection = 0

        if sim == True:
            print("Simulation (no inst., rand. temp)")
        else:
            try:
                self.rm = pyvisa.ResourceManager()
                print("Found resources: {}" .format(self.rm.list_resources()))
            except:
                print("ERROR with initialization.")
            
            print("Trying to connect")
            while connection == 0:
                # will continue to try to connect
                try:
                    self.inst = self.rm.open_resource("USB0::0x2A8D::0x5001::MY58004219::0::INSTR",
                                                            read_termination = "\n", 
                                                            write_termination = "\n")
                    response = self.instrument.query("?IDN")
                    print("Instrument response to ?IDN: {}".format(response))
                
                    if response != "ERROR":
                        self.connection = 1
      
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
                except:
                    print("Unknown error.")

                time.sleep(2)

        print("Done!")


if __name__ == "__main__":
    inst = pyVisDAQ(sim = False)