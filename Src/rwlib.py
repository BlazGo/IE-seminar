import configparser
import os
import time
import datetime

class fileFunc():
    """ Class with functions to read/write to a file 
    
    Functions:
                - __init__ (define all variables on one place)
                - read_config (reads the configuration file (config.ini, 
                  has to be in the same folder as scripts))
                - wait_file (waits for the specified file to be created in
                  order to continue)
                - create_file (creates the files)
                - check_outputf_exists (checks if the output filename
                  already exists )
                - write_heading (copies the first 8 lines of text, adds to
                  the front additional info and additional T columns in
                  accordance to the number of channels)

                - close_files (closes both open files)
                """

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
        # Input:
        #       - configuration filename (optional default already set)
        
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

    def wait_file(self):
        # Will stay in loop until the file to read is created.

        i = 0
        # Check if file exists
        while not os.path.exists(self.INPUT_FILEPATH):
            time.sleep(1)

            if i == 0:
                print("[INFO] Waiting for file to read")
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
            raise ValueError("[ERROR] {} isn't a file!".format(self.INPUT_FILEPATH))
        
        self.output_file = open(self.OUTPUT_FILEPATH, 'x')
        print("[INFO] File: {} created.".format(self.OUTPUT_FILENAME))

    def check_f_exists(self, filepath=self.OUTPUT_FILEPATH):
       # Checks if the defined output file already exists
       # Output:
       #    - bool (True, False)

        if os.path.exists(filepath):
            print("[WARN] File to create with this name already exists!")
            print("       {}".format(filepath))
            return True
        else:
            return False

    def write_heading(self):
        # Parse the heading and write to new file

        # Additional info
        start_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        additional_info = "Start time: {}\tInstrument: {}\t Meas num: {}\t Wait time: {}\n".format(start_time,
                                                                                                  self.INSTRUMENT_NAME,
                                                                                                  self.MEAS_NUM,
                                                                                                  self.WAIT_TIME
                                                                                                  )
        # Read the file
        input_lines = self.input_file.readlines()
        heading = input_lines[0:8] # It is defined as first 8 rows
        heading[-1] = heading[-1].rstrip("\n") # Remove new line from last line

        # For each channel new column
        for c in range(1, self.CHANNEL_NUM+2):
            heading[-1] += "\tT{} (°C)".format(c)

        heading[-1] += "\n"

        # Write the heading
        self.output_file.writelines(additional_info)
        self.output_file.writelines(heading)
                
    def read_lastline(self):
        # Reads the last line in file
        line = None # Referenced before assignment error
        for line in self.input_file:
            pass
        self.new_line = line

    def check_newline(self):
        if self.new_line == self.old_line:
            return True
        elif self.new_line != self.old_line:
            return False

    def parse_line(self, og_line=self.new_line, temps=-1):
        temp_string = ""
        
        # For each temp
        for num in temps:
            temp_string += "\t" + str(round(num, 2))
        
        # Add the temperatures at the end of the line
        return og_line.strip("\n") + temp_string + "\n"

    def write_line(self, temp=-1):
        string_to_write = self.parse_line(self.new_line, temp)
        self.output_file.write(string_to_write)
        self.output_file.flush()

        self.line_num += 1
        print("[INFO] Written line {}".format(self.line_num))

    def close_files(self):
        print("[INFO] Closing files")
        self.input_file.close()
        self.output_file.close()


if __name__ == "__main__":
    
    fileFunc = fileFunc()
    fileFunc.read_config()

    if fileFunc.check_f_exists(fileFunc.OUTPUT_FILEPATH) == True:
        raise ValueError

    fileFunc.create_file()
    fileFunc.write_heading()
    
    try:
        while True:
            fileFunc.read_lastline()
            if fileFunc.check_newline() == False:
                fileFunc.write_line([1, 2])
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        pass

    fileFunc.close_files()