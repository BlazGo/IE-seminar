import pyvisa as pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt



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
    def __init__(self, meas_num=11, wait_time=1, channels_start=101, channels_end=105, graph=False):
        """ Initializes instrument resources

        Init method to initialize pyvisa resource manager and set measurement
        parameters. (TODO: Graph, show measurements in real time)
        """
        self.rm = pyvisa.ResourceManager()
        print(f"[INFO] Found resources: {self.rm.list_resources()}")

        self.MEAS_NUM = meas_num
        self.WAIT_TIME = wait_time
        self.CHANNELS_START = channels_start
        self.CHANNELS_END = channels_end
        self.CHANNELS_NUM = channels_end - channels_start +1
        self.GRAPH = graph

        # self.inst.query_delay = 0.0 # Doesnt do much 0.0 default
        # lowest it can go ~140ms for 10 channels
        time.sleep(0.5)

    def init_inst(self):
        """ Initializes the session with the instrument
        
        Initializes the session, select the first found
        resource.
        TODO: selection what instrument to use or always
        find the default one (Keysight DAQ970A)
        """
        try:
            resource = self.rm.list_resources()[0]
        except:
            resource = "USB0::0x2A8D::0x5001::MY58004219::0::INSTR"
            print(f"[INFO] Setting default Instrument address. Check response.")

        self.inst = self.rm.open_resource(resource,
                                           read_termination = "\n", 
                                           write_termination = "\n")
        self.inst.timeout = 4000
        print("[INFO] Instrument initialized")

    def check_response(self):
        """ Returns instument response 
        
        Sends command to send the instrument indetification
        (usually name, brand, etc)
        """
        response = self.inst.query("*IDN?")
        print(f"[INFO] Instrument response to *IDN?: {response}")
        return response

    def scan_channels(self):
        """ Scans channel and returns/selects connected ones
        
        TODO: Automatic detection
        """
        # if nothing is connected value -9.9e+37
        # Start and end channels should consider all possible channels
        self.channel_start = 101
        self.channel_end = 111
        self.channel_num = self.channel_end - self.channel_start

    def acquire_measurements(self):
        """ Function to return measurement

        Can define the channels and number of measurements.
        Returns array 
        rows->channels 
        column->measurements
        """

        Tcouple = "J"
        resolution = "0.01"
        channels = f"{self.CHANNELS_START}:{self.CHANNELS_END}"
        command = f"MEASure:TEMPerature:TCouple? {Tcouple},{resolution},(@{channels})"
               
        self.temp_array = np.zeros((self.MEAS_NUM, self.CHANNELS_NUM))
        meas_iteration = 1
        while meas_iteration <= self.MEAS_NUM:
            print(f"Current iteration: {meas_iteration}")
            start = time.time()

            temp_raw = self.inst.query_ascii_values(command)
            
            print(f"Instrument time: {round((time.time()-start)*1000,3)} [ms]")

            for i in range(0, len(temp_raw)):
                self.temp_array[meas_iteration-1,i] = temp_raw[i]

            meas_iteration += 1
        
        return self.temp_array

    def process_measurements(self):
        """ Measurement process
        Simple statistical process of data. Reads the median,
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
        temp_array_raw = np.asarray(self.temp_array)
        medians = np.median(temp_array_raw, axis = 0)
        # print(f"Shape: {np.shape(temp_array_raw)}, Medians: {np.shape(medians)}")

        temp_whole = []
        for channel in range(0, self.CHANNELS_NUM):
            # Check each channel column
            temp_temp = []
            for measurement in temp_array_raw[:,channel]:
                # Check each measurement row
                diff = measurement - medians[channel]
                if (abs(diff) <= 0.2):
                    temp_temp.append(measurement)
            temp_whole.append(temp_temp)

        processed_temp = []
        for channel in temp_whole:
            processed_temp.append(np.mean(np.asarray(channel)))
        
        self.channel_temps = processed_temp
        return self.channel_temps

    def get_measurements(self):
        self.acquire_measurements()
        self.process_measurements()

    def close_session(self):
        """ Closes instrument session
        The correct way to disconnect/close instrument. If it is not
        executed properly the instrument "stays" in the memmory and
        in the next program run it can detect it even when not connected.

        """
       
        try:
            self.inst.close()
            print(f"[INFO] Session closed")
        except pyvisa.errors.InvalidSession:
            print(f"[WARN] Invalid session. The resource might be closed.")

    def graph(self):
        """ Graph data in real time
        TODO
        """
        #plt.plot(self.temp_array)
        #plt.show()

        #print(self.channel_temps)
        if self.GRAPH == True:
            fig, ax = plt.subplots()
            ax.plot(range(0, self.CHANNELS_NUM), self.channel_temps)
            ax.grid()
            plt.show()

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

if __name__ == "__main__":
    """ Test run
    Should print the measurements if everything works. 

    """
    
    try:
        inst = KeyDAQ(meas_num=17, graph=True)

        inst.init_inst()
        inst.scan_channels()

        meas_time = time.time()
        inst.acquire_measurements()
        print(f"Meas time: {round((time.time()-meas_time)*1000,3)} [ms]")

        calc_time = time.time()
        inst.process_measurements()
        print(f"Calc time: {round((time.time()-calc_time)*1000,3)} [ms]")
        
        inst.close_session()

    except KeyboardInterrupt as e:
        print(f"Keyboard interrupt {e}")
        inst.close_session()