import pyvisa as pyvisa
import time
import numpy as np

class KeyDAQ():
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        print("Found resources: {}" .format(self.rm.list_resources()))

        self.inst = self.rm.open_resource("USB0::0x2A8D::0x5001::MY58004219::0::INSTR",
                                           read_termination = "\n", 
                                           write_termination = "\n")
        self.meas_num = 11
        self.meas_time = 1

        self.inst.timeout = 4000
        #self.inst.query_delay = 0 # Doesnt do much lowest it can go ~140ms for 10 channels
        # better to set to 0.1 and get ~105-220ms per channels scan just in case

        time.sleep(0.5)
        response = self.inst.query("*IDN?")
        print("Instrument response to *IDN?: {}".format(response))

    def scan_channels(self):
        # if nothing is connected value -9.9e+37
        self.channel_start = 101
        self.channel_end = 111
        self.channel_num = self.channel_end - self.channel_start

    def get_temp(self):
        Tcouple = "J"
        resolution = "0.01"
        channels = "{}:{}".format(self.channel_start, self.channel_end)
        command = "MEASure:TEMPerature:TCouple? {},{},(@{})".format(Tcouple, 
                                                                    resolution, 
                                                                    channels)
        
        self.temp_array = np.zeros((self.meas_num, self.channel_num))

        meas_iteration = 1
        while meas_iteration <= self.meas_num:
            print("Current iteration: {}".format(meas_iteration))
            start = time.time()
            temp_raw = self.inst.query_ascii_values(command)
            print("Instrument time: {} [ms]".format(round((time.time()-start)*1000,3)))

            for i in range(0, len(temp_raw)-1):
                self.temp_array[meas_iteration-1,i] = temp_raw[i]

            meas_iteration += 1

        #print(self.temp_array)

    def meas_process(self):
        temp_array_raw = np.asarray(self.temp_array)
        shape = np.shape(temp_array_raw)
        print(shape)

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
        print(processed_temp)
        self.channel_temps = processed_temp
        return self.channel_temps

    def close_session(self):
        self.rm.close()
        try:
            print("Found resources: {}" .format(self.rm.list_resources()))
        except pyvisa.errors.InvalidSession: # error when thereis invalid session
            print("Session closed")

if __name__ == "__main__":
    inst = KeyDAQ()
    inst.scan_channels()

    meas_time = time.time()
    inst.get_temp()
    print("Meas time: {} [ms]".format(round((time.time()-meas_time)*1000,3)))

    calc_time = time.time()
    inst.meas_process()
    print("Calc time: {} [ms]".format(round((time.time()-calc_time)*1000,3)))

    inst.close_session()