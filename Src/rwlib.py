import configparser
import os
import time
from datetime import datetime


class fileFunc:
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
        """ Initialize all variables
        Initialize all variables used in a wider scope in
        the __init__ function first.

        """

        self.INPUT_DIR_PATH = "EMPTY"
        self.INPUT_FILENAME = "EMPTY"
        self.OUTPUT_DIR_PATH = "EMPTY"
        self.OUTPUT_FILENAME = "EMPTY"

        self.INPUT_FILE_PATH = "EMPTY"
        self.OUTPUT_FILE_PATH = "EMPTY"

        self.INSTRUMENT_NAME = "EMPTY"
        self.INSTRUMENT_ADDRESS = "EMPTY"

        self.MEAS_NUM = "EMPTY"
        self.WAIT_TIME = "EMPTY"
        self.TOLERANCE = "EMPTY"

        self.CHANNELS_START = "EMPTY"
        self.CHANNELS_END = "EMPTY"
        self.CHANNEL_NUM = "EMPTY"

        # Other variables
        self.input_file = None
        self.output_file = None
        self.last_line = None
        self.line_num = 0

    def read_config(self, config_filename="config.ini"):
        """ Reads the configuration file and saves parameters as
        class variables. Config file to be in the same directory
        as the running scripts.

        Parameters:
        ----------
        config_filename : configuration filename (optional default already set)

        """

        print("[INFO] Reading config file")

        # Get absolute path (should be safe to move)
        path = '/'.join((os.path.abspath(__file__).replace('\\','/')).split('/')[:-1])

        config = configparser.ConfigParser()
        config.read(os.path.join(path, config_filename))

        # Define the keys of config file
        file_setup = config["FILE_SETUP"]
        instrument_setup = config["INSTRUMENT_SETUP"]
        measurement_setup = config["MEASUREMENT_SETUP"]

        # Retrieve all the (needed) variables
        self.INPUT_DIR_PATH = file_setup.get("input_dir_path")
        self.INPUT_FILENAME = file_setup.get("input_filename")
        self.OUTPUT_DIR_PATH = file_setup.get("output_dir_path")
        self.OUTPUT_FILENAME = file_setup.get("output_filename")

        # For convenience join the dir path and filename
        self.INPUT_FILE_PATH = os.path.join(self.INPUT_DIR_PATH, self.INPUT_FILENAME)
        self.OUTPUT_FILE_PATH = os.path.join(self.OUTPUT_DIR_PATH, self.OUTPUT_FILENAME)

        self.INSTRUMENT_NAME = instrument_setup.get("instrument")
        self.INSTRUMENT_ADDRESS = instrument_setup.get("instrument_address")
        self.CHANNELS_START = int(instrument_setup.get("channels_start"))
        self.CHANNELS_END = int(instrument_setup.get("channels_end"))
        self.CHANNEL_NUM = self.CHANNELS_END - self.CHANNELS_START + 1

        self.MEAS_NUM = int(measurement_setup.get("meas_num"))
        self.WAIT_TIME = float(measurement_setup.get("wait_time"))
        self.TOLERANCE = float(measurement_setup.get("tolerance"))
        self.ASYNC_TEMP = bool(measurement_setup.get("async_temp"))

    def wait_file(self, filepath, filename=""):
        """ Waits for specified file to be created.

        Parameters:
        ----------
        filepath : string (path)
            File path.
        filename : string (name)
            File name.

        """

        print(f"[INFO] Waiting for file: {filename} to be created.")
        # Check if file exists
        while not os.path.exists(filepath):
            time.sleep(0.5)

        print(f"[INFO] File: {filename} found.")

    def create_file(self, ifilepath, ifilename, ofilepath, ofilename):
        """ Create the file to write
        First waits for read file to be created then creates the
        output file and opens the original file.

        Parameters:
        ----------
        ifilepath : string (path)
            Input file path.
        ifilename : string (name)
            Input file name.
        ofilepath : string (path)
            Output file path.
        ofilename : string (name)
            Output file name.

        """
        
        # Waiting for the input file to be created
        self.wait_file(ifilepath, ifilename)

        self.output_file = open(ofilepath, 'x')
        self.input_file = open(ifilepath, 'r')
        print(f"[INFO] File: {ofilename} created.")
 
    def write_heading(self, heading_lines=8):
        """ Writes the heading. Copies the first N lines,
        adds additional parameters as the first line, adds
        another tab/column at the last line and writes
        everything into the new file 

        Parameters:
        ----------
        heading_lines : int
            Number of lines to copy (our case default=9).
        
        """

        # Additional info
        start_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        additional_info = f"Start time: {start_time},\tInstrument: {self.INSTRUMENT_NAME}, Address: {self.INSTRUMENT_ADDRESS}\n"
        additional_info_1 = f"Meas num: {self.MEAS_NUM},\tWait time: {self.WAIT_TIME} [s],\tTolerance: {self.TOLERANCE} [°C]\n"

        print(f"[INFO] Waiting for heading.")

        csum = 0
        while csum < heading_lines:
            time.sleep(0.5)
            temp = self.input_file.readlines() # Reading lines "consumes" them next read will be from the last read line
            csum = csum + len(temp)
        print(f"[INFO] Heading reached 8 lines. Continuing.")

        # Read the file
        self.input_file.seek(0)  # File pointer reset to beginning
        heading = self.input_file.readlines()[0:heading_lines]  # It is defined as first 8 rows
        # Remove new line from last line
        heading[-1] = heading[-1].rstrip("\n")

        # For each channel new column
        for c in range(1, self.CHANNEL_NUM+2):
            heading[-1] += f"\tT{c} (°C)"

        heading[-1] += "\n"  # Add line break at the end of last line

        # Write the heading
        self.output_file.writelines(additional_info)
        self.output_file.writelines(additional_info_1)
        self.output_file.writelines(heading)
        self.last_line = self.read_last_line()  # Save the last (heading) line as last line
        # or the last measurement in the past

    def read_last_line(self):
        """ Reads the last line of the file.

        Returns:
        ----------
        line : str
        
        """
        line = None  # Referenced before assignment error
        # reads last line in file
        # Faster than file.readlines()[-1]
        for line in self.input_file:
            pass
        return line

    def check_newline(self):
        """ Checks the last line of the file. If a change
        in the last line is detected it saves the last line.

        Returns:
        ----------
        Status : Bool
            If a change is detected returns True. If there is no
            change in last line returns False
        
        """
        
        line = self.read_last_line()

        if line == None:
            return False
        if line == self.last_line:
            return False
        elif line != self.last_line:
            # Save new line as current line to check
            self.last_line = line
            return True

    def write_new_line(self, original_line="", temperatures=-1):
        """ Writes new line into the output file. Joins old line and
        formats the temperatures.

        Parameters:
        ----------
        original_line : string
            In our case we input the last line read.
        temperatures : list
            List containing numbers (floats).
        
        """

        temp_string = ""
        for num in temperatures:
            temp_string += "\t" + str(round(num, 3))

        # Remove newline from old line, add temp and new line
        string_to_write = original_line.strip("\n") + temp_string + "\n"

        self.output_file.write(string_to_write)
        # Flush the buffer so it immediately writes the line
        self.output_file.flush()

        # Keep track of written lines
        self.line_num += 1

    def close_files(self):
        """ Closes both files the correct way.

        """
        
        print("[INFO] Closing files")
        self.input_file.close()
        self.output_file.close()

    

if __name__ == "__main__":

    fc = fileFunc()
    fc.read_config()

    fc.create_file(fc.INPUT_FILE_PATH, fc.INPUT_FILENAME,
                   fc.OUTPUT_FILE_PATH, fc.OUTPUT_FILENAME)
    fc.write_heading()

    try:
        while True:
            print("[INFO] In main loop...")
            if fc.check_newline() == True:
                fc.write_new_line(fc.last_line, [1, 2, 3, 4])
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

    fc.close_files()
