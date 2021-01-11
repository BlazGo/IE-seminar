import pyvisa as pyvisa
import time
import numpy as np

"""
Known errors:
    - watch out for initialization. Everything can hang with no errors
    if the bitness of the libraries is incompatible
    pyvisa-info (usefull command)
    try to use ivi backend
    - Keysight DAQ970 driver same bitness as OS
    - working with python 64-bit (was the problem with 32-bit python?)
"""

class KeyDAQ():
    
    def __init__(self, meas_num=11, wait_time=1, channels_start=101, channels_end=105):
        self.rm = pyvisa.ResourceManager()
        print(f"Found resources: {self.rm.list_resources()}")

        self.MEAS_NUM = meas_num
        self.WAIT_TIME = wait_time
        self.CHANNELS_START = channels_start
        self.CHANNELS_END = channels_end
        self.CHANNELS_NUM = channels_end - channels_start

        #self.inst.query_delay = 0.0 # Doesnt do much lowest it can go ~140ms for 10 channels 0.0 default
        time.sleep(0.5)

    def init_inst(self):
        self.inst = self.rm.open_resource("USB0::0x2A8D::0x5001::MY58004219::0::INSTR",
                                           read_termination = "\n", 
                                           write_termination = "\n")
        self.inst.timeout = 4000

    def check_response(self):
        response = self.inst.query("*IDN?")
        print(f"[INFO] Instrument response to *IDN?: {response}")

    def scan_channels(self):
        # if nothing is connected value -9.9e+37
        self.channel_start = 101
        self.channel_end = 111
        self.channel_num = self.channel_end - self.channel_start

    def acquire(self):
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

            for i in range(0, len(temp_raw)-1):
                self.temp_array[meas_iteration-1,i] = temp_raw[i]

            meas_iteration += 1

    def process(self):
        temp_array_raw = np.asarray(self.temp_array)
        shape = np.shape(temp_array_raw)
        #print(shape)

        medians = np.median(temp_array_raw, axis = 1)
        
        temp_whole = []
        for column in range(0, shape[0]):
            temp_temp = []
            for row in range(0, shape[1]):
                diff = temp_array_raw[column, row] - medians[column]
                if (abs(diff) <= 0.4):
                    temp_temp.append(temp_array_raw[column, row])
            temp_whole.append(temp_temp)

        processed_temp = []
        for channel in temp_whole:
            processed_temp.append(np.mean(np.asarray(channel)))

        #print(temp_whole)
        #print(processed_temp)
        self.channel_temps = processed_temp
        return self.channel_temps

    def close_session(self):
        self.rm.close()
        try:
            print(f"Found resources: {self.rm.list_resources()}")
        except pyvisa.errors.InvalidSession: # error when thereis invalid session
            print(f"Session closed")

if __name__ == "__main__":
    try:
        inst = KeyDAQ()
        inst.init_inst()
        inst.scan_channels()

        meas_time = time.time()
        inst.acquire()
        print(f"Meas time: {round((time.time()-meas_time)*1000,3)} [ms]")

        calc_time = time.time()
        inst.process()
        print(f"Calc time: {round((time.time()-calc_time)*1000,3)} [ms]")
        
        inst.close_session()
        
    except KeyboardInterrupt as e:
        print(f"Keyboard interrupt {e}")
        inst.close_session()