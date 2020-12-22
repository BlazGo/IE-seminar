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

    def __init__(self, sim=False, meas_num=11, meas_time=1):
        """ Initialization
        Sets up a connection with the instrument
        """

        self.start_time = datetime.now()
        print("\n---------------------------------------------------")
        print("Initializing instrument resources...")

        self.sim = sim
        # measurement parameters
        self.meas_num = meas_num    # [/] number of measurements in time frame
        self.meas_time = meas_time  # [s] time for all measurements 
        self.temp = 20              # [°C] initialize temp (for simulation, inst overrides)
        self.tol = 0.3              # [°C] tolerance for outliers
        # SCPI command settings
        self.Tcouple = "J"          # define type of Termo couple
        self.resolution = "0.01"    # resolution (not sure if it actually applies)
        self.channels = "105:107"   # what channels to scan

        connection = 0

        if self.sim == True:
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
                    print("[ERROR] Problem with instrument IO.")
                    print("----------------------------------------------------")
                    time.sleep(5)
                except ValueError:
                    print("----------------------------------------------------")
                    print("[ERROR] Problem with instrument Values.")
                    print("----------------------------------------------------")
                    time.sleep(5)
                except:
                    print("Unknown error.")
                    time.sleep(5)
        print("Done!")

    def set_parameters(self):
        """ Set up parameters 
        Set parameters of instrument and consequently measurement parameters
        """
        print("Setting up instrument...")
        # delay after sent command after to continue
        self.inst.query_delay = self.meas_time  # [s]    
        # time before timeout error 
        self.inst.timeout = 10000  # [ms]               
        print("Done.")

    def meas_process(self, T_lsit):
        """
        Input:
            - list of temperatures
        Output:
            - processed temp
        We first use median to remove outliers with certain tolerance.
        Then mean is calculated from the remaining temperatures.
        It is strongly recommended to use more than 10 measurements
        and that it is an odd number. It could happen with too strict
        tolerance and wild measurements that no measurement would satisfy
        the criteria.
        """
        T_arr = np.array(T_lsit)
        median = np.median(T_arr)

        new_meas = []

        for temp in T_lsit:
            diff = median - temp
            if abs(diff) < self.tol:
                new_meas.append(temp)

        avg_temp = np.mean(np.array(new_meas))
        print("Temperature: {}".format(avg_temp))
        return avg_temp

    def get_temp(self):
        """
        Input:
            - meas_num (number of measurement for one returned temp)
            - meas_time (time avalible for all the measurements)
        Output:
            - temperature (float)
        
        "MEASure:TEMPerature:TCouple? J,0.01,(@105:107)"
        """

        time_for_one = self.meas_time/self.meas_num     # divide given time with number of measurements
        command = "MEASure:TEMPerature:TCouple? {},{},(@{})".format(self.Tcouple, 
                                                                    self.resolution, 
                                                                    self.channels)
        meas_list = []

        if self.sim == False:
            try:
                # iterate over the given number of measurements
                for measurement in range(0, self.meas_num):
                    self.temp = self.temp = self.inst.query_ascii_values(command)
                    meas_list.append(self.temp)
            except:
                print("ERROR with measurement.")
                self.temp = -1
        else:
            for measurement in range(0, self.meas_num):
                self.temp = self.temp + (random.randrange(0, 10) -5)/10
                meas_list.append(self.temp)
                time.sleep(time_for_one)

        self.temp = self.meas_process(meas_list)
        return self.temp

    def close_session(self):
        """
        Properly closes session with the instrument
        (Or else it can still be saved even if device is no tconnected)
        """

        print("Clossing session with instrument...")
        self.rm.close()
        print("Done.")

        end_time = datetime.now()
        print("\n---------------------------------------------------")
        print("Start time: {}\n".format(end_time.strftime("%Y/%m/%d %H:%M:%S")))

if __name__ == "__main__":
    # if everything works no errors should be raised
    
    inst = pyVisDAQ(sim = True)

    start = time.time()
    print("Test temp: {0:.4f}".format(inst.get_temp()))
    print(round((time.time() - start), 4))

    # when simulated no ninstrument is initialized
    if inst.sim == False:
        inst.close_session()