print("Running test_data_creator")

from datetime import date
import os
from os import listdir
from os.path import isfile, join
import time
import tkinter as tk
from tkinter import filedialog

"""

- Opens template file and reads it
- Creates new file
    - Copies heading and adds T [°C]
    - In loop writes new lines in intervals

"""

original_file_path = "C:/Users/blazg/Dekstop/FE_faks/3-Semester/SRM-Seminar_iz_robotike_in_merjenj/Code/N4877 AM550 Core 303 230V 50Hz temp R.MTREZ"
original_file_path = filedialog.askopenfilename()
path_to_create = "C:/Users/blazg/Dekstop/FE_faks/3-Semester/SRM-Seminar_iz_robotike_in_merjenj/Code/"

# Quality of life code checks the files of specific name and adds the next index increment
counter = 0
filename = path_to_create + "new.txt"
#filename = path_to_create + str(date.today()) + "_Test_{}.txt" 
while isfile(filename.format(counter)):
    counter += 1
filename_to_create = filename.format(counter)

# Open the template file and read the contents
with open(original_file_path, "r") as og_file:
    original_lines = og_file.readlines()

new_file = open("new.txt", "x")

# Heading edit and write
heading = original_lines[0:8]
new_file.writelines(heading)
new_file.flush() # without it the file most of the time does not update until the program finishes 
# TODO implement function that handles all the writing procedures and line processing

time.sleep(5)
for i in range(8,len(original_lines)):
    start = time.time()
    new_file.write(original_lines[i]) # write i-th line
    #print(original_lines[i])
    new_file.flush() # refresh file? update
    print("Time of loop: ", round((time.time()-start)*1000,4), "[ms]")
    time.sleep(2)