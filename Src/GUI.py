import tkinter as tk
import os
import time
from datetime import datetime

from instlib import KeyDAQ
from rwlib import fileFunc

def do_nothing():
    print("Something")

class measUI:
    """
    docstring
    """

    def __init__(self):

        #self.instrument = KeyDAQ()
        self.rwfunc = fileFunc()
        self.rwfunc.read_config()
        self.initUI()

    def initUI(self):
        self.root = tk.Tk()
        self.root.title("Merjenje temperature")
        self.root.geometry("800x350")

        self.btn_setup = tk.Button(self.root, text = "Nastavi", command = self.create_subwindow)
        btn_start = tk.Button(self.root, text = "Start", command = self.start_program)
        btn_abort = tk.Button(self.root, text = "Abort", command = self.abort)

        self.lbl_clock = tk.Label(self.root, text = "*clock*")

        # Descriptions display
        lbl_file_setup = tk.Label(self.root, text = "File setup")
        lbl_in_dir = tk.Label(self.root, text = "Input file folder path")
        lbl_in_name = tk.Label(self.root, text = "Input filename")
        lbl_out_dir = tk.Label(self.root, text = "Output file folder path")
        lbl_out_name = tk.Label(self.root, text = "Output filename")

        lbl_meas_setup = tk.Label(self.root, text = "Measurement setup")
        lbl_inst_name = tk.Label(self.root, text = "Instrument")
        lbl_meas_num = tk.Label(self.root, text = "Measurement number")
        lbl_channels = tk.Label(self.root, text = "Channels")
        lbl_wait_time = tk.Label(self.root, text = "Wait time")
        lbl_units = tk.Label(self.root, text = "[seconds]")
        
        # Values display
        self.lbl_in_dirD = tk.Label(self.root, text = self.rwfunc.INPUT_DIR_PATH)
        self.lbl_in_nameD = tk.Label(self.root, text = self.rwfunc.INPUT_FILENAME)
        self.lbl_out_dirD = tk.Label(self.root, text = self.rwfunc.OUTPUT_DIR_PATH)
        self.lbl_out_nameD = tk.Label(self.root, text = self.rwfunc.OUTPUT_FILENAME)
       
        self.lbl_inst_nameD = tk.Label(self.root, text = self.rwfunc.INSTRUMENT_NAME)
        self.lbl_meas_numD = tk.Label(self.root, text = self.rwfunc.MEAS_NUM)
        channels = f"{self.rwfunc.CHANNELS_START}:{self.rwfunc.CHANNELS_END}"
        self.lbl_channelsD = tk.Label(self.root, text = channels)
        self.lbl_wait_timeD = tk.Label(self.root, text = self.rwfunc.WAIT_TIME)

        # Place widgets
        self.lbl_clock.grid(row = 0, column = 2)
        lbl_file_setup.grid(row = 1, column = 0)
        lbl_in_dir.grid(row = 2, column = 0)
        lbl_in_name.grid(row = 3, column = 0)
        lbl_out_dir.grid(row = 4, column = 0)
        lbl_out_name.grid(row = 5, column = 0)
        lbl_meas_setup.grid(row = 6, column = 0)
        lbl_inst_name.grid(row = 7, column = 0)
        lbl_meas_num.grid(row = 8, column = 0)
        lbl_channels.grid(row = 9, column = 0)
        lbl_wait_time.grid(row = 10, column = 0)
        lbl_units.grid(row = 10, column = 2)

        self.lbl_in_dirD.grid(row = 2, column = 1)
        self.lbl_in_nameD.grid(row = 3, column = 1)
        self.lbl_out_dirD.grid(row = 4, column = 1)
        self.lbl_out_nameD.grid(row = 5, column = 1)
        self.lbl_inst_nameD.grid(row = 7, column = 1)
        self.lbl_meas_numD.grid(row = 8, column = 1)
        self.lbl_channelsD.grid(row = 9, column = 1)
        self.lbl_wait_timeD.grid(row = 10, column = 1)

        self.btn_setup.grid(row = 1, column = 2)
        btn_abort.grid(row = 11, column = 0)
        btn_start.grid(row = 11, column = 2)

        self.update_time()
        self.root.mainloop()        
        
        print(self.rwfunc.INPUT_DIR_PATH)

    def create_subwindow(self):
        """ Function to create config subwindow """
        self.subwin = tk.Toplevel()

        lbl_file_setup = tk.Label(self.subwin, text = "File setup")
        lbl_in_dir = tk.Label(self.subwin, text = "Input file folder path")
        lbl_in_name = tk.Label(self.subwin, text = "Input filename")
        lbl_out_dir = tk.Label(self.subwin, text = "Output file folder path")
        lbl_out_name = tk.Label(self.subwin, text = "Output filename")

        lbl_meas_setup = tk.Label(self.subwin, text = "Measurement setup")
        lbl_inst_name = tk.Label(self.subwin, text = "Instrument")
        lbl_meas_num = tk.Label(self.subwin, text = "Measurement number")
        lbl_start = tk.Label(self.subwin, text = "Start")
        lbl_end = tk.Label(self.subwin, text = "End")
        lbl_channels = tk.Label(self.subwin, text = "Channels")
        lbl_wait_time = tk.Label(self.subwin, text = "Wait time")
        lbl_units = tk.Label(self.subwin, text = "[seconds]")

        self.ent_in_dir = tk.Entry(self.subwin)
        self.ent_in_dir.insert(0, self.rwfunc.INPUT_DIR_PATH)
        self.ent_in_name = tk.Entry(self.subwin)
        self.ent_in_name.insert(0, self.rwfunc.INPUT_FILENAME)
        self.ent_out_dir = tk.Entry(self.subwin)
        self.ent_out_dir.insert(0, self.rwfunc.OUTPUT_DIR_PATH)
        self.ent_out_name = tk.Entry(self.subwin)
        self.ent_out_name.insert(0, self.rwfunc.OUTPUT_FILENAME)

        self.ent_inst_name = tk.Entry(self.subwin)
        self.ent_inst_name.insert(0, self.rwfunc.INSTRUMENT_NAME)
        self.spi_meas_num = tk.Spinbox(self.subwin, to = 21)
        self.spi_meas_num.delete(0, "end")
        self.spi_meas_num.insert(0, self.rwfunc.MEAS_NUM)
        self.spi_ch_start = tk.Spinbox(self.subwin)
        self.spi_ch_start.insert(0, self.rwfunc.CHANNELS_START)
        self.spi_ch_end = tk.Spinbox(self.subwin)
        self.spi_ch_end.insert(0, self.rwfunc.CHANNELS_END)
        self.spi_wtime = tk.Spinbox(self.subwin)
        self.spi_wtime.insert(0, self.rwfunc.WAIT_TIME)

        btn_reset = tk.Button(self.subwin, text = "reset", command = do_nothing)
        btn_save_return = tk.Button(self.subwin, text = "Save and return", command = self.save_and_return)

        lbl_file_setup.grid(row = 0, column = 0)
        lbl_in_dir.grid(row = 1, column = 0)
        lbl_in_name.grid(row = 2, column = 0)
        lbl_out_dir.grid(row = 3, column = 0)
        lbl_out_name.grid(row = 4, column = 0)
        lbl_meas_setup.grid(row = 5, column = 0)
        lbl_inst_name.grid(row = 6, column = 0)
        lbl_meas_num.grid(row = 7, column = 0)
        lbl_start.grid(row = 8, column = 1)
        lbl_end.grid(row = 8, column = 2)
        lbl_channels.grid(row = 9, column = 0)
        lbl_wait_time.grid(row = 10, column = 0)
        lbl_units.grid(row = 10, column = 2)
        
        self.ent_in_dir.grid(row = 1, column = 1, columnspan = 2)
        self.ent_in_name.grid(row = 2, column = 1, columnspan = 2)
        self.ent_out_dir.grid(row = 3, column = 1, columnspan = 2)
        self.ent_out_name.grid(row = 4, column = 1, columnspan = 2)

        self.ent_inst_name.grid(row = 6, column = 1)
        self.spi_meas_num.grid(row = 7, column = 1)
        self.spi_ch_start.grid(row = 9, column = 1)
        self.spi_ch_end.grid(row = 9, column = 2)
        self.spi_wtime.grid(row = 10, column = 1)

        btn_reset.grid(row = 0, column = 1)
        btn_save_return.grid(row = 11, column = 3)

    def save_and_return(self):
        """ Saves all the variables back into the appropriate class """
        self.rwfunc.INPUT_DIR_PATH = self.ent_in_dir.get()
        self.rwfunc.INPUT_FILENAME = self.ent_in_name.get()
        self.rwfunc.INPUT_FILE_PATH = os.path.join(self.rwfunc.INPUT_DIR_PATH, self.rwfunc.INPUT_FILENAME)
        
        self.rwfunc.OUTPUT_DIR_PATH = self.ent_out_dir.get()
        self.rwfunc.OUTPUT_FILENAME = self.ent_out_name.get()
        self.rwfunc.OUTPUT_FILE_PATH = os.path.join(self.rwfunc.OUTPUT_DIR_PATH, self.rwfunc.OUTPUT_FILENAME)

        self.rwfunc.INSTRUMENT_NAME = self.ent_inst_name.get()
        self.rwfunc.MEAS_NUM = self.spi_meas_num.get()
        self.rwfunc.CHANNELS_START = self.spi_ch_start.get()
        self.rwfunc.CHANNELS_END = self.spi_ch_end.get()
        self.rwfunc.WAIT_TIME = self.spi_wtime.get()

        self.lbl_in_dirD.config(text = self.rwfunc.INPUT_DIR_PATH)
        self.lbl_in_nameD.config(text = self.rwfunc.INPUT_FILENAME)
        self.lbl_out_dirD.config(text = self.rwfunc.OUTPUT_DIR_PATH)
        self.lbl_out_nameD.config(text = self.rwfunc.OUTPUT_FILENAME)
        self.lbl_inst_nameD.config(text = self.rwfunc.INSTRUMENT_NAME)
        self.lbl_meas_numD.config(text = self.rwfunc.MEAS_NUM)
        channels = f"{self.rwfunc.CHANNELS_START}:{self.rwfunc.CHANNELS_END}"
        self.lbl_channelsD.config(text = channels)
        self.lbl_wait_timeD.config(text = self.rwfunc.WAIT_TIME)

        # Close the subwindow
        self.subwin.destroy()

    def abort(self):
        print("[INFO] Closing")
        exit()

    def start_program(self):
        self.btn_setup.grid_remove()
        curr_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        print(f"[INFO] Start time: {curr_time}")

        if self.rwfunc.check_f_exists(self.rwfunc.OUTPUT_FILE_PATH) == True:
            raise ValueError

        self.rwfunc.create_file(self.rwfunc.INPUT_FILE_PATH,
                                self.rwfunc.INPUT_FILENAME,
                                self.rwfunc.OUTPUT_FILE_PATH,
                                self.rwfunc.OUTPUT_FILENAME)
        self.rwfunc.write_heading()
        
        self.main_loop()
        
    def main_loop(self):
        start = time.time()
        print("[INFO] In loop")
        
        try:
            while True:
                self.rwfunc.read_lastline()

                if self.rwfunc.check_newline() == True:
                    self.rwfunc.write_line([1, 2])
                elif self.rwfunc.check_newline() == False:
                    time.sleep(self.rwfunc.WAIT_TIME)

        except KeyboardInterrupt:
            print("Stopping...")
            pass

        #print(time.time()-start)
        #self.root.after(1000, self.main_loop)

    def update_time(self):
        #start = time.time()
        self.lbl_clock.config(text = datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        self.root.after(500, self.update_time)
        #print(f"Time taken: {(time.time()-start)*1000}")
    
if __name__ == "__main__":
    measUI = measUI()
    print("*---------------------------------------------------------------------*")
    print("Parameters:")
    for key in measUI.rwfunc.__dict__:
        print(f"{key}:\t-->\t{measUI.rwfunc.__dict__[key]}")