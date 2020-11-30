#!/usr/bin/python
# -*- coding: UTF-8

from os.path import join, isfile
from os import listdir
import time
import random
from datetime import date

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

        if file_to_read == None:
            self.file_to_read = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/%s_Test_0.txt" % today
        else:
            self.file_to_read = file_to_read

        if folder_to_create == None:
            self.folder_to_create = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/"
        else:
            self.folder_to_create = folder_to_create
        
        if filename_to_create == None:
            base_filename = "_New_"
            counter = 0
            filename = self.folder_to_create + str(date.today()) + base_filename + "{}.txt" 
            while isfile(filename.format(counter)):
                counter += 1
            self.filename_to_create = filename.format(counter)
        else:
            self.filename_to_create = filename_to_create

        print("Initialized...")

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
        heading = self.old_file.readlines()[0:8]
        heading[-1] = heading[-1].rstrip("\n") + "T (°C)\n" # add temperature "column"
        self.new_file.writelines(heading)

    def close_files(self):
        print("Closing files...")
        self.old_file.close()
        self.new_file.close()
        print("Done.")

rw = read_write_Func()
rw.wait_file()
rw.copy_heading()
rw.close_files()
"""
file_to_read = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/%s_Test_0.txt" % date.today()
path_to_create = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/"
base_filename = "_New_"
index = len([i for i in listdir(path_to_create) if isfile(join(path_to_create, i)) and base_filename in i])

counter = 0
filename = path_to_create + str(date.today()) + base_filename + "{}.txt" 
while isfile(filename.format(counter)):
    counter += 1
filename_to_create = filename.format(counter)
print(filename_to_create)

# Loop to wait if the file hasnt been created yet
while True:
    try:
        old_file = open(file_to_read, "r")
        print("File created")
        break
    except:
        print("No file created yet")
        time.sleep(2)
        pass

new_file = open(filename_to_create, "a")

# Heading copy
heading = old_file.readlines()[0:8]
print(len(heading))
heading[-1] = heading[-1].rstrip("\n") + "T (°C)\n" # add temperature "column"
new_file.writelines(heading)

# Loop variables
temp = 20
previous_line = None
last_line = None
while True:
    start = time.time() # Loop timing
    temp = temp + random.randint(-10, 10) / 10 # calculate random temperature

    # Try statement if no lines are written yet
    try:
        for line in old_file:
            pass
        last_line = line
    except:
        print("Error with lines")

    # Check if the new line is different
    if last_line == previous_line:
        print("No new line...")
    elif last_line != previous_line:
        new_file.write(last_line .strip("\n") + "\t" + str(round(temp, 2)) + "\n") # Vrite the read line and add temperature at the end
        print("New line written... %s" %last_line)

    # Save the current line as previous
    previous_line = last_line
    print(round((time.time()-start)*1000,3))
    time.sleep(1)
    """