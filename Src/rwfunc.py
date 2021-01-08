import configparser
import os
import time
import datetime

class fileFunc():
    """ Class with functions to read and write to a file """

    def __init__(self):
        """ Initialize all variables """

        # All variables used in wider scope are defined here first
        # and are changed later in the operation

        # Constants (while running the main loop)
        # Also the variables which are for the user to define
        self.INPUT_DIR_PATH = "EMPTY"
        self.INPUT_FILENAME = "EMPTY"
        self.OUTPUT_DIR_PATH = "EMPTY"
        self.OUTPUT_FILENAME = "EMPTY"

        self.INPUT_FILE_PATH = "EMPTY"
        self.OUTPUT_FILE_PATH = "EMPTY"

        self.INSTRUMENT_NAME = "EMPTY"
        self.MEAS_NUM = "EMPTY"
        self.WAIT_TIME = "EMPTY"
        self.CHANNELS_START = "EMPTY"
        self.CHANNELS_END = "EMPTY"

        self.CHANNEL_NUM = "EMPTY"

        # Other variables
        self.input_file = None
        self.output_file = None
        self.new_line = None
        self.old_line = None
        self.line_num = 0

    def read_config(self, name="config.ini"):
        # Reads the configuration file and saves variables
        print("[INFO] Reading config file")

        # Get absolute path (should be safe to move)
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        
        config = configparser.ConfigParser()
        config.read(os.path.join(path, name))

        # Define the keys of config file
        file_setup = config["FILE_SETUP"]            
        instrument_setup = config["INSTRUMENT_SETUP"]

        # Retrieve all the (needed) variables
        self.INPUT_DIR_PATH = file_setup.get("Input_dir_path")
        self.INPUT_FILENAME = file_setup.get("Input_filename")
        self.OUTPUT_DIR_PATH = file_setup.get("Output_dir_path")
        self.OUTPUT_FILENAME = file_setup.get("Output_filename")

        self.INSTRUMENT_NAME = instrument_setup.get("Instrument_name")
        self.MEAS_NUM = int(instrument_setup.get("Meas_num"))
        self.WAIT_TIME = float(instrument_setup.get("Wait_time"))
        self.CHANNELS_START = int(instrument_setup.get("Channels_start"))
        self.CHANNELS_END = int(instrument_setup.get("Channels_end"))

        # For convenience join the dir path and filename
        self.INPUT_FILEPATH = os.path.join(self.INPUT_DIR_PATH, self.INPUT_FILENAME)
        self.OUTPUT_FILEPATH = os.path.join(self.OUTPUT_DIR_PATH, self.OUTPUT_FILENAME)

        self.CHANNEL_NUM = self.CHANNELS_END - self.CHANNELS_START

        print("[INFO] Done")

    def wait_file(self):
        # Will stay in loop until the file to read is created.
        print("[INFO] Waiting for file to read")

        i = 0
        # Check if file exists
        while not os.path.exists(self.INPUT_FILEPATH):
            time.sleep(1)
            if i >= 6:
                print("[INFO] File not yet found.")
                i = 0
            i += 1
        print("[INFO] File: {} found".format(self.INPUT_FILENAME))

    def create_file(self):
        # First waits for read file to be created, then opens it
        # and creates the file to write to.

        # Waiting for the input file to be created
        self.wait_file()

        # If it is a file -> open
        if os.path.isfile(self.INPUT_FILEPATH):
            self.input_file = open(self.INPUT_FILEPATH, 'r')
        else:
            raise ValueError("[ERROR] {} isn't a file!".format(file_path))
        
        self.output_file = open(self.OUTPUT_FILEPATH, 'x')
        print("[INFO] File created.")

    def check_outputf_exists(self):
       # Checks if the defined output file already exists
        if os.path.exists(self.OUTPUT_FILEPATH):
            print("[WARN] File to create with this name already exists!")
            print("       {}".format(self.OUTPUT_FILEPATH))
            return True
        else:
            print("[INFO] File to create with this name doesnt exist.")
            return False

    def write_heading(self):
        # Parse the heading and write to new file

        # Additional info
        start_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        addiional_info = "Start time: {}\tInstrument: {}\t Meas num: {}\t Wait time: {}\n".format(start_time,
                                                                                                  self.INSTRUMENT_NAME,
                                                                                                  self.MEAS_NUM,
                                                                                                  self.WAIT_TIME
                                                                                                  )
        # Read the file
        input_lines = self.input_file.readlines()
        heading = input_lines[0:8] # It is defined as first 8 rows
        heading[-1] = heading[-1].rstrip("\n")

        # For each channel new column
        for c in range(1, self.CHANNEL_NUM+2):
            heading[-1] += "\tT{} (°C)".format(c)

        heading[-1] += "\n"

        # Write the heading
        self.output_file.writelines(additional_info)
        self.output_file.writelines(heading)
        
    def read_lastline(self):
        pass

    def check_newline(self):
        pass

    def parse_line(self):
        pass

    def write_line(self):
        pass

    def close_files(self):
        self.input_file.close()
        self.output_file.close()

if __name__ == "__main__":
    
    fileFunc = fileFunc()
    fileFunc.read_config()

    if fileFunc.check_outputf_exists() == True:
        raise ValueError

    fileFunc.create_file()
    fileFunc.write_heading()

    print("Done")