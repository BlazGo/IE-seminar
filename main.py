#!/usr/bin/python
# -*- coding: UTF-8

from os.path import join, isfile
from os import listdir
import time
import random
from datetime import date
from visaRes import VisVmeter
import tkinter.filedialog
import tkinter as tk

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

def browse_button():
    folder = tk.filedialog.askdirectory()
    print(folder)

class read_write_Func():

    """
    Simple class to organize used functions
    """
    
    def __init__(self):
        #today = date.today()
        self.interval = 1 # seconds interval of repetition
        self.curr_line = None
        self.old_line = None
        self.instrument = VisVmeter()
        self.lines_written = 0

        config_path = "C:/Users/b_gorjanc/Documents/Project_2/default_config.txt"
        
        with open(config_path, "r") as config:
            config_lines = config.readlines()
            self.folder_to_read = config_lines[1]
            self.filename_to_read = config_lines[4]
            self.folder_to_create = config_lines[7]
            self.filename_to_create = config_lines[10]
            pass

        print("\nFolder to read: {}File to read: {}Folder to write: {}New filename: {}\n".format(self.folder_to_read, 
                                                                                                self.filename_to_read, 
                                                                                                self.folder_to_create, 
                                                                                                self.filename_to_create))

        print("Initialized...\n")

    def wait_file(self):
        status = 0
        # check if wanted file is already created and read it if not wait.
        while status == 0:
            try:
                self.old_file = open(join(self.folder_to_read, self.filename_to_read), "r")
                self.new_file = open(self.folder_to_create, self.filename_to_create, "a")
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

rw = read_write_Func()

root = tk.Tk()
text1 = tk.Label(root, text = rw.folder_to_read)
text1.pack()
button1 = tk.Button(root, text = "Browse for folder", command = browse_button)
button1.pack()
tk.mainloop()

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