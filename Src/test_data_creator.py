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

class file_create():

    def __init__(self):

        self.window = tk.Tk()

        btn_get_original_filename = tk.Button(
            text = "Izberi original datoteko",
            command = self.get_original_filename,
            )

        btn_get_new_file_path = tk.Button(
            text = "Izberi direktorijo",
            command = self.get_new_file_path,
            )

        btn_continue = tk.Button(
            text = "Nadaljuj",
            command = self.close_continue,
            )

        btn_get_original_filename.pack()
        btn_get_new_file_path.pack()
        btn_continue.pack()

        self.window.mainloop()

    def close_continue(self):
        print("Data recorded. Continuing...")
        self.window.destroy()

    def get_original_filename(self):
        self.original_file_path = filedialog.askopenfilename()

    def get_new_file_path(self):
        self.new_file_path = filedialog.askdirectory()

    def create(self):
        with open(self.original_file_path, "r") as og_file:
            self.original_lines = og_file.readlines()
        
        counter = 0
        filename = self.new_file_path + "/new.txt"
        while isfile(filename.format(counter)):
            counter += 1
        filename_to_create = filename.format(counter)
        self.new_file = open(filename_to_create, "x")
        print("Created heading.")

    def create_heading(self):
        heading = self.original_lines[0:8]
        self.new_file.writelines(heading)
        self.new_file.flush()

    def main_loop(self):
        print("Entered main loop...")
        for i in range(8,len(self.original_lines)):
            self.new_file.write(self.original_lines[i]) # write i-th line
            self.new_file.flush() # refresh file? update
            time.sleep(4)
            print("New line written\t{}".format(time.time()))


fc = file_create()
fc.create()
fc.create_heading()
fc.main_loop()