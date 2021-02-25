import time
import random
import numpy as np
import pyvisa

#import matplotlib.pyplot as plt


class KeyDAQ():
    """
    Known errors:
        - watch out for initialization. Everything can hang with no errors
        if the bitness of the libraries is incompatible
        pyvisa-info (usefull command)
        try to use ivi backend
        - Keysight DAQ970 driver same bitness as OS
        - working with python 64-bit (the problem 32-bit python only?)

    """

    def __init__(self, meas_num=11, channels_start=101, channels_end=105, tolerance=1.0, graph=False, simulation=False):
        """ Initializes instrument resources
        Init method to initialize pyvisa resource manager and set measurement
        parameters.

        Parameters
        ----------
        meas_num : int
            Numer of readings to take per one measurement.
        channels_start : int
            Starting channel to scan
        channels_end : int
            Ending channel to scan
        tolerance : float
            Measurement tolerance for outliers.
        graph : bool
            Show graph

        If the starting channel and the ending channel are the same we
        specify later on in the measurement function the correct form.

        Tolerance is a condition for outliers. Any measurement that deviates
        from the median for more than the specified tolerance will be ignored.

        TODO: Graph, show measurements in real time

        """
        
        self.rm = pyvisa.ResourceManager()
        print(f"[INFO] Found resources: {self.rm.list_resources()}")

        self.MEAS_NUM = meas_num
        self.CHANNELS_START = channels_start
        self.CHANNELS_END = channels_end
        self.CHANNELS_NUM = channels_end - channels_start +1

        self.TOLERANCE = tolerance
        self.GRAPH = graph
        self.SIMULATION = simulation
        # self.inst.query_delay = 0.0 # Doesnt do much 0.0 default
        # lowest it can go ~140ms for 10 channels
        time.sleep(0.5)

    def init_inst(self, resource="USB0::0x2A8D::0x5001::MY58004219::0::INSTR"):
        """ Initializes the session with the instrument
        
        Parameters
        ----------
        resource : string
            The address of the instrument with which the 
            session will be opened.

        """
        
        if self.SIMULATION == True:
            print(f"[INFO] Using simulation.")
            return
        else:
            print(f"[INFO] Opening resource: {resource}")
            try:
                self.inst = self.rm.open_resource(resource,
                                            read_termination = "\n", 
                                            write_termination = "\n")
                self.inst.timeout = 120000 # [ms]
                print("[INFO] Instrument initialized")
            except pyvisa.errors.VisaIOError:
                print(f"[ERROR] Insufficient location information or the requested device or resource is not present in the system.")
                raise     
            except Exception as e:
                print(e)
                raise

    def check_response(self):
        """ Returns instument response 
        
        Sends command for instrument to send its identification
        (usually name, brand, etc.)

        Returns:
        ----------
        response : string
            response to *IDN?
        
        """
        if self.SIMULATION == True:
            return "Simulation without instrument", self.get_measurements()
        elif self.SIMULATION == False: 
            try:   
                response = self.inst.query("*IDN?")
                #print(f"[INFO] Instrument response to *IDN?: {response}")
                return response, self.get_measurements()
            except Exception as e:
                print(e)
                return f"[WARN] Error occured {e}", "None"

    def scan_channels(self, channels_min=101, channels_max=119):
        """ Scans all detected channels and tries to detect connected ones.

        Parameters:
        ----------
        channels_min : int
        channels_max : int

        Returns:
        ----------
        channel_temps : list of numbers
            processed temperatures [list 1xCHANNEL_NUM]
        TODO not yet implemented

        """

        # if nothing is connected value -9.9e+37
        # Start and end channels should consider all possible channels
        # scan_list = f"@({channels_min}:{channels_max})"
        channel_candidates = []
        return channel_candidates

    def acquire_measurements(self):
        """ Function to return measurement
        Each column represents one channel, one row represents
        measurement of all channels at one time.    

        Returns:
        ----------
        meas_array : array of numbers (floats)
            measurements per channel [MEAS_NUMxCHANNEL_NUM]
        
        """

        if self.SIMULATION == True:
            sim_meas = np.random.uniform(low=18.0, high=22.0, size=(self.MEAS_NUM, self.CHANNELS_NUM))
            """
            meas = np.around(sim_meas[:,0], 1)
            print(meas)
            median = np.median(meas)
            print(median)
            meas = np.where(1<abs(meas-median), meas, 0)
            meas = np.ma.masked_equal(meas,0)
            print(meas)
            meas = np.mean(meas)
            print(meas)
            """
            return sim_meas

        Tcouple = "J"
        resolution = "0.01"
        
        channels = f"{self.CHANNELS_START}:{self.CHANNELS_END}"
        if self.CHANNELS_START == self.CHANNELS_END:
            channels = f"{self.CHANNELS_START}"

        command = f"MEASure:TEMPerature:TCouple? {Tcouple},{resolution},(@{channels})"
               
        meas_array = np.zeros((self.MEAS_NUM, self.CHANNELS_NUM))

        for meas_iteration in range(0, self.MEAS_NUM):
            temp_raw = self.inst.query_ascii_values(command)
            for i in range(0, len(temp_raw)):
                meas_array[meas_iteration, i] = temp_raw[i]

        return meas_array

    def process_measurements(self, measurements):
        """ Simple statistical process of data. Reads the median,
        removes outliers and returns avg. of each channel. 

        Parameters:
        ----------
        measurements : list of lists
            Embedded lists 1xCHANNEL_NUM measurements. Len of 
            parent list is based on MEAS_NUM.

        Returns:
        ----------
        channel_temps : list of numbers
            processed temperatures [list 1xCHANNEL_NUM]
        
        """

        temp_array_raw = np.asarray(measurements)
        medians = np.median(temp_array_raw, axis = 0)

        temp_whole = []
        for channel in range(0, self.CHANNELS_NUM):
            # Check each channel column
            temp_temp = []
            for measurement in temp_array_raw[:,channel]:
                # Check each measurement row
                diff = measurement - medians[channel]
                if (abs(diff) <= self.TOLERANCE):
                    temp_temp.append(measurement)
            temp_whole.append(temp_temp)

        processed_temp = []
        for channel in temp_whole:
            processed_temp.append(np.mean(np.asarray(channel)))
        
        self.channel_temps = processed_temp
        return processed_temp

    def get_measurements(self):
        raw_measurements = self.acquire_measurements()
        processed_measurements = self.process_measurements(raw_measurements)
        return processed_measurements

    def close_session(self):
        """ Closes instrument session
        The correct way to disconnect/close instrument. If it is not
        executed properly the instrument "stays" in the memmory and
        in the next program run it can detect it even when not connected.

        """
       
        try:
            self.rm.close()
            if self.SIMULATION == False:
                self.inst.close()
            print(f"[INFO] Session closed")
        except pyvisa.errors.InvalidSession:
            print(f"[WARN] Invalid session. The resource might be closed.")

    def graph(self):
        """ Graph data in real time
        TODO not implemented yet.
        """
        """
        if self.GRAPH == True:
            plt.plot(range(0, self.CHANNELS_NUM), self.channel_temps)
            plt.show()
        """

    def setup_inst(self):
        """ Inst. measurement parameters setup.
        TODO
        Function that sets up the instrument to correct parameters
        if necessary. For temperature measurements the instrument selects range internally
        you cannot select which range is used.

        For Tcouple meas. the inst. selects 100mV range.
        Tcouple meas. require a reference junction temp. see:
        SENSe TEMPerature:TRANsducer:TCouple:RJUNction:TYPE command
        By default a fixed ref.junction temp of 0°C is used
        """
        # CONFigure and MEASure command automatically selsects °C
        self.inst.query(f"UNIT:TEMP C,(@{self.CHANNELS_START}:{self.CHANNELS_END})")
        self.inst.query(f"TEMP:TRANS:TC:RJUN:TYPE INT, (@{self.CHANNELS_START}:{self.CHANNELS_END})")

    def scan_resources(self):
        """ Scan connected devices

        Returns:
        ----------
        res_list : tuple of connnected devices
        
        """
        rm_scan = pyvisa.ResourceManager()
        res_list = rm_scan.list_resources()
        rm_scan.close()
        return res_list

if __name__ == "__main__":
    """ Test run
    Should print the measurements if everything works. 

    """
    
    try:
        inst = KeyDAQ(meas_num=17, simulation=False)

        inst.init_inst()
        inst.scan_channels()

        meas_time = time.time()
        measurements = inst.get_measurements()
        print(f"Measurement time: {round((time.time()-meas_time)*1000,3)} [ms]")
        print(measurements)

        inst.close_session()

    except KeyboardInterrupt as e:
        print(f"Keyboard interrupt {e}")
        inst.close_session()