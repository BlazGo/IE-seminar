#!/usr/bin/python
# -*- coding: UTF-8

from os.path import join, isfile
from os import listdir
import time
import random
from datetime import date
from visaRes import VisVmeter

print("Starting python script...")

"""
Script that reads the defined file line by line and adds temperature at the end.
It also copies the first 8 lines at the beginning (heading) and at the end also
adds temperature "column".

Waits for the file to be created to create its own file and starts copying 
line by line.
"""

class read_write_Func():

    """
    Simple class to organize used functions
    """
    
    def __init__(self, file_to_read = None, folder_to_create = None, filename_to_create = None, add_date = 1):
        today = date.today()
        self.interval = 2 # seconds interval of repetition
        self.curr_line = None
        self.old_line = None
        self.instrument = VisVmeter()
        self.lines_written = 0

        # Set default names or save the input
        if file_to_read is None:
            self.file_to_read = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/%s_Test_0.txt" % today
        else:
            self.file_to_read = file_to_read

        if folder_to_create is None:
            self.folder_to_create = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/"
        else:
            self.folder_to_create = folder_to_create
        
        if filename_to_create is None:
            base_filename = "_New_"
            counter = 0
            filename = self.folder_to_create + str(date.today()) + base_filename + "{}.txt" 
            while isfile(filename.format(counter)):
                counter += 1
            self.filename_to_create = filename.format(counter)
        else:
            self.filename_to_create = filename_to_create

        print("Initialized...\n")

    def wait_file(self):
        status = 0
        # check if wanted file is already created and read it if not wait.
        while status == 0:
            try:
                self.old_file = open(self.file_to_read, "r")
                self.new_file = open(self.filename_to_create, "a")
                print("File created. Moving on...")
                break
            except:
                print("No file created yet. Waiting...")
                time.sleep(self.interval)
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
            temp = self.instrument.getMeasurement() # Get temp value
            self.copy_line(self.new_file, self.curr_line, temp)

        self.old_line = self.curr_line
        self.lines_written += 1
    
    def copy_line(self, file_to_write, line, temp = 0):
        file_to_write.write(line.strip("\n") + "\t" + str(round(temp, 2)) + "\n") # Vrite the read line and add temperature at the end
        print("Line %i written..." % int(self.lines_written))

    def close_files(self):
        # Close both open files
        print("Closing files...")
        self.old_file.close()
        self.new_file.close()
        print("Done.")

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