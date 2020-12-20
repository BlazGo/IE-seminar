#!/usr/bin/python
# -*- coding: UTF-8

import os
import time
import random
import configparser
from visaRes import VisVmeter
from GUI import simpleUI


print("Starting python script...")

"""
Script that reads the defined file line by line and adds temperature at the end.
It also copies the first 8 lines at the beginning (heading) and at the end also
adds temperature "column".

Waits for the file to be created to create its own file and starts copying 
line by line.

Add to heading also what we use

read used parameters from config file
"""

class read_write_Func():

    """
    Simple class to organize used functions
    """
    
    def __init__(self):
        self.interval = 1 # seconds interval of repetition
        self.curr_line = None
        self.old_line = None
        self.lines_written = 0

        self.Tmeter = VisVmeter()

        self.Input_dir_path = ""
        self.Input_filename = ""
        self.Output_dir_path = ""
        self.Output_filename = ""
        self.Instrument_type = ""       

        try:
            config = configparser.ConfigParser()
            config.read("meas_setup.ini")

            file_setup  = config["FILE_SETUP"]            
            instrument_setup = config["INSTRUMENT_SETUP"]

            self.Input_dir_path = file_setup.get("Input_dir_path")
            self.Input_filename = file_setup.get("Input_filename")
            self.Output_dir_path = file_setup.get("Output_dir_path")
            self.Output_filename = file_setup.get("Output_filename")

            self.Instrument_type = instrument_setup.get("Instrument")
            self.Meas_num = int(instrument_setup.get("Meas_num"))
            self.Meas_time = float(instrument_setup.get("Meas_time"))
            
            print("Read config file parameters.")

        except:
            print("Possible error with configuration.")
            pass

        print("\nDefault:\nFolder to read: {}\nFile to read: {}\nFolder to write: {}\nNew filename: {}\nInstrument: {}\n".format(
            self.Input_dir_path,     
            self.Input_filename, 
            self.Output_dir_path, 
            self.Output_filename,
            self.Instrument_type)
            )

        input_parameters = {
            "Input dir path"    : self.Input_dir_path,
            "Input filename"    : self.Input_filename,
            "Output dir path"   : self.Output_dir_path,
            "Output filename"   : self.Output_filename,
            "Instrument"        : self.Instrument_type
            }

        UI = simpleUI(input_parameters)
        new_parameters = UI.output_parameter_list

        self.Input_dir_path = new_parameters.get("Input dir path")
        self.Input_filename = new_parameters.get("Input filename")
        self.Output_dir_path = new_parameters.get("Output dir path")
        self.Output_filename =  new_parameters.get("Output filename")
        self.Instrument_type = new_parameters.get("Instrument")

        print("Initialized...\n")

    def wait_file(self):
        # check if wanted file is already created and read it if not wait.
        while True:
            try:
                self.old_file = open(os.path.join(self.Input_dir_path, self.Input_filename), "r")
                self.new_file = open(self.Output_dir_path, self.Output_filename, "a")
                print("File created. Moving on...")
                break
            except:
                print("No file created yet. Waiting...")
                time.sleep(2)
                pass
    
    def copy_heading(self):
        # Copies the first eight ines and adds Temperature symbol at the end
        heading = self.old_file.readlines()[0:8]
        heading[-1] = heading[-1].rstrip("\n") + "T (°C)\n" # add temperature "column"
        self.new_file.writelines(heading)

    def check_for_newline(self):
        # get last line in file
        try:
            for line in self.old_file:
                pass
            self.curr_line = line
        except:
            print("No lines to copy yet...")
            pass

        if self.curr_line is self.old_line:
            print("No new line...")
        elif self.curr_line is not self.old_line:
            print("New line detected. Writing...")
            temp = self.Tmeter.getMeasurement() # Get temp value
            self.copy_line(self.new_file, self.curr_line, temp)
            self.old_line = self.curr_line
    
    def copy_line(self, file_to_write, line, temp = 0):
        file_to_write.write(line.strip("\n") + "\t" + str(round(temp, 2)) + "\n") # Vrite the read line and add temperature at the end
        self.lines_written += 1
        print("Line %i written..." % int(self.lines_written))

    def close_files(self):
        # Close both open files
        print("Closing files...")
        self.old_file.close()
        self.new_file.close()
        print("Done.")


if __name__ == "__main__":
        
    rw = read_write_Func()
    rw.wait_file()
    rw.copy_heading()

    try:
        while True:
            start = time.time() # Loop timing
            rw.check_for_newline()
            print("Time taken: %.3f [ms]\n" % round((time.time()-start)*1000,3))
            time.sleep(rw.interval)

    except KeyboardInterrupt:
        print("Stopping...")
        pass

    rw.close_files()