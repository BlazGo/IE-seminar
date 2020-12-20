print("Running test_data_creator")

from datetime import date
from os import listdir
from os.path import isfile, join
import time

"""

- Opens template file and reads it
- Creates new file
    - Copies heading and adds T [°C]
    - In loop writes new lines in intervals

"""

original_file_path = "C:/Users/b_gorjanc/Documents/Project_2/N4877 AM550 Core 303 230V 50Hz temp R.MTREZ"
path_to_create = "C:/Users/b_gorjanc/Documents/Project_2/Measurement_files/"

# Quality of life code checks the files of specific name and adds the next index increment
counter = 0
filename = path_to_create + "N4877 AM550 Core 303 230V 50Hz temp R.txt"
#filename = path_to_create + str(date.today()) + "_Test_{}.txt" 
while isfile(filename.format(counter)):
    counter += 1
filename_to_create = filename.format(counter)

# Open the template file and read the contents
with open(original_file_path, "r") as og_file:
    original_lines = og_file.readlines()
new_file = open(filename_to_create, "x")

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