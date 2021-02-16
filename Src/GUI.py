import os
import sys
import time
import threading
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Custom libraries
from instlib import KeyDAQ
from rwlib import fileFunc


def do_nothing():
    # Placeholder for buttons
    print("Something")

def curr_time():
    # Returns current time in string format
    return datetime.now().strftime("%H:%M:%S %d/%m/%Y")


class measUI():
    """
    Class with UI definition 
    """

    def __init__(self, SIM=False):

        # Simulation not implemented
        # Best solution to replace instrument calls with
        # random number generator manually
        self.SIM = SIM

        # Widget padding
        self.padx = 6
        self.pady = int(self.padx/2)
        # Color definitions
        self.color_bg = "#212121"
        self.color_bg_s = "#1F2933"
        self.color_lbl = "#323F4B"
        self.color_disp = "#334E68"
        self.color_text = "#F5F7FA"
        self.color_btn = "#627D98"

        # Font definitions
        self.font_L = ('Leelawadee UI', 16)
        self.font_M = ('Leelawadee UI', 14)
        self.font_I = ('Consolas', 12)

        # Initiate class for files
        self.rwfunc = fileFunc()
        # Read config file and set parameters
        self.rwfunc.read_config()

        self.create_mainwindow()
        # Start clock update
        self.update_time()
        # Start main UI loop
        self.root.mainloop()

    def create_mainwindow(self):
        """ Function that handles main window geometry
        """
        # Define UI basics
        self.root = tk.Tk()
        self.root.title("Merjenje temperature")
        self.root.minsize(1416, 540)
        #self.root.geometry("750x360")
        self.root.configure(bg = self.color_bg)

        f_frame = tk.Frame(self.root, bg = self.color_bg_s, relief = "sunken")
        m_frame = tk.Frame(self.root, bg = self.color_bg_s, relief = "sunken")

        # Descriptions display
        self.lbl_clock = tk.Label(self.root, text = "*clock*", width = 18, font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_console = tk.Label(self.root, text = "Console", font = self.font_L,  bg = self.color_lbl, fg = self.color_text) 

        lbl_file_setup = tk.Label(self.root, text = "File setup", font = self.font_L,  bg = self.color_lbl, fg = self.color_text)        
        lbl_in_dir = tk.Label(f_frame, text = "Input file folder path", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_in_name = tk.Label(f_frame, text = "Input filename", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_out_dir = tk.Label(f_frame, text = "Output file folder path", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_out_name = tk.Label(f_frame, text = "Output filename", font = self.font_M, bg = self.color_lbl, fg = self.color_text)

        lbl_meas_setup = tk.Label(self.root, text = "Measurement setup", font = self.font_L, bg = self.color_lbl, fg = self.color_text)        
        lbl_inst_name = tk.Label(m_frame, text = "Instrument", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_meas_num = tk.Label(m_frame, text = "Measurement number", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_channels = tk.Label(m_frame, text = "Channels", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_chan_des = tk.Label(m_frame, text = "Start:End", bg = self.color_bg, fg = self.color_text)
        lbl_wait_time = tk.Label(m_frame, text = "Wait time", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_units = tk.Label(m_frame, text = "[seconds]", bg = self.color_bg, fg = self.color_text)
        
        # Values display
        self.lbl_in_dirD = tk.Label(f_frame, text = self.rwfunc.INPUT_DIR_PATH, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")
        self.lbl_in_nameD = tk.Label(f_frame, text = self.rwfunc.INPUT_FILENAME, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")
        self.lbl_out_dirD = tk.Label(f_frame, text = self.rwfunc.OUTPUT_DIR_PATH, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")
        self.lbl_out_nameD = tk.Label(f_frame, text = self.rwfunc.OUTPUT_FILENAME, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")
       
        self.lbl_inst_nameD = tk.Label(m_frame, text = self.rwfunc.INSTRUMENT_NAME, font = self.font_I, width = 25, bg = self.color_disp, fg = self.color_text, relief = "sunken")
        self.lbl_meas_numD = tk.Label(m_frame, text = self.rwfunc.MEAS_NUM, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")

        channels = f"{self.rwfunc.CHANNELS_START}:{self.rwfunc.CHANNELS_END}"
        self.lbl_channelsD = tk.Label(m_frame, text = channels, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")
        self.lbl_wait_timeD = tk.Label(m_frame, text = self.rwfunc.WAIT_TIME, font = self.font_I, bg = self.color_disp, fg = self.color_text, relief = "sunken")

        # Buttons
        self.btn_setup = tk.Button(self.root, text = "Configure", command = self.create_subwindow, font = self.font_M, width = 18, bg = self.color_btn, fg = self.color_text)
        btn_start = tk.Button(self.root, text = "Start", command = self.start_program, font = self.font_M, width = 18, bg = self.color_btn, fg = self.color_text)
        btn_abort = tk.Button(self.root, text = "Abort", command = self.abort, font = self.font_M, width = 18, bg = self.color_btn, fg = self.color_text)
        btn_check_inst = tk.Button(m_frame, text = "Check inst", command = self.check_instrument, font = self.font_M, width = 18, bg = self.color_btn, fg = self.color_text)

        self.txt_console = tk.Text(self.root, height = 25, font = self.font_I, width = 80)

        # Place widgets
        self.lbl_clock.grid(row = 0, column = 1, sticky = "e", padx = self.padx, pady = self.pady)
        lbl_console.grid(row = 0, column = 2, sticky = "ew", padx = self.padx, pady = self.pady)

        f_frame.grid(row = 2, column = 0, columnspan = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        m_frame.grid(row = 7, column = 0, columnspan = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        
        lbl_file_setup.grid(row = 1, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_in_dir.grid(row = 2, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_in_name.grid(row = 3, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_out_dir.grid(row = 4, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_out_name.grid(row = 5, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        
        lbl_meas_setup.grid(row = 6, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_inst_name.grid(row = 7, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_meas_num.grid(row = 8, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_channels.grid(row = 9, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_chan_des.grid(row = 9, column = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_wait_time.grid(row = 10, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_units.grid(row = 10, column = 2, sticky = "ew", padx = self.padx, pady = self.pady)

        self.lbl_in_dirD.grid(row = 2, column = 1, columnspan = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_in_nameD.grid(row = 3, column = 1, columnspan = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_out_dirD.grid(row = 4, column = 1, columnspan = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_out_nameD.grid(row = 5, column = 1, columnspan = 2, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_inst_nameD.grid(row = 7, column = 1, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_meas_numD.grid(row = 8, column = 1, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_channelsD.grid(row = 9, column = 1, sticky = "ew", padx = self.padx, pady = self.pady)
        self.lbl_wait_timeD.grid(row = 10, column = 1, sticky = "ew", padx = self.padx, pady = self.pady)

        self.btn_setup.grid(row = 0, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        btn_abort.grid(row = 11, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        btn_start.grid(row = 11, column = 1, sticky = "e", padx = self.padx, pady = self.pady)        
        btn_check_inst.grid(row = 7, column = 2, sticky = "e", padx = self.padx, pady = self.pady)

        self.txt_console.grid(row = 1, column = 2, rowspan = 11, sticky = "w", padx = self.padx, pady = self.pady)

    def create_subwindow(self):
        """ Function that handles configuration subwindow
        """
        # Define window basic parameters
        self.subwin = tk.Toplevel(bg = self.color_bg)
        self.subwin.title("Nastavitve")
        #self.subwin.geometry("700x350")

        f_frame = tk.Frame(self.subwin, bg = self.color_bg_s)
        m_frame = tk.Frame(self.subwin, bg = self.color_bg_s)

        # Label widgets
        lbl_file_setup = tk.Label(self.subwin, text = "File setup", font = self.font_L, bg = self.color_lbl, fg = self.color_text)
        lbl_in_dir = tk.Label(f_frame, text = "Input file folder path", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_in_name = tk.Label(f_frame, text = "Input filename", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_out_dir = tk.Label(f_frame, text = "Output file folder path", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_out_name = tk.Label(f_frame, text = "Output filename", font = self.font_M, bg = self.color_lbl, fg = self.color_text)

        lbl_meas_setup = tk.Label(self.subwin, text = "Measurement setup", font = self.font_L, bg = self.color_lbl, fg = self.color_text)
        lbl_inst_name = tk.Label(m_frame, text = "Instrument", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_meas_num = tk.Label(m_frame, text = "Measurement number", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_start = tk.Label(m_frame, text = "Start", bg = self.color_lbl, fg = self.color_text)
        lbl_end = tk.Label(m_frame, text = "End", bg = self.color_lbl, fg = self.color_text)
        lbl_channels = tk.Label(m_frame, text = "Channels", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_wait_time = tk.Label(m_frame, text = "Wait time", font = self.font_M, bg = self.color_lbl, fg = self.color_text)
        lbl_units = tk.Label(m_frame, text = "[seconds]", bg = self.color_lbl, fg = self.color_text)

        # Entry widgets
        self.ent_in_dir = tk.Entry(f_frame, width = 90, font = self.font_I)
        self.ent_in_dir.insert(0, self.rwfunc.INPUT_DIR_PATH)
        self.ent_in_name = tk.Entry(f_frame, width = 90, font = self.font_I)
        self.ent_in_name.insert(0, self.rwfunc.INPUT_FILENAME)

        self.ent_out_dir = tk.Entry(f_frame, width = 90, font = self.font_I)
        self.ent_out_dir.insert(0, self.rwfunc.OUTPUT_DIR_PATH)
        self.ent_out_name = tk.Entry(f_frame, width = 90, font = self.font_I)
        self.ent_out_name.insert(0, self.rwfunc.OUTPUT_FILENAME)

        self.ent_inst_name = tk.Entry(m_frame, font = self.font_I)
        self.ent_inst_name.insert(0, self.rwfunc.INSTRUMENT_NAME)
    
        # Spinbox widgets
        meas_num_valid = tuple(range(1, 22, 2))
        self.spi_meas_num = tk.Spinbox(m_frame, values = meas_num_valid, font = self.font_I)
        self.spi_meas_num.delete(0, "end")
        self.spi_meas_num.insert(0, self.rwfunc.MEAS_NUM)

        self.spi_ch_start = tk.Spinbox(m_frame, from_ = 0, to = 999, font = self.font_I)
        self.spi_ch_start.delete(0, "end")
        self.spi_ch_start.insert(0, self.rwfunc.CHANNELS_START)
    
        self.spi_ch_end = tk.Spinbox(m_frame, from_ = 0, to = 999, font = self.font_I)
        self.spi_ch_end.delete(0, "end")
        self.spi_ch_end.insert(0, self.rwfunc.CHANNELS_END)

        self.spi_wtime = tk.Spinbox(m_frame, from_ = 0.5, to = 20, increment = 0.1, font = self.font_I)
        self.spi_wtime.delete(0, "end")
        self.spi_wtime.insert(0, self.rwfunc.WAIT_TIME)

        # Button widgets
        btn_reset = tk.Button(self.subwin, text = "Reset", command = do_nothing, width = 18, font = self.font_M, bg = self.color_btn, fg = self.color_text)
        btn_save_return = tk.Button(self.subwin, text = "Save and return", command = self.save_and_return, width = 18, font = self.font_M, bg = self.color_btn, fg = self.color_text)
        btn_cin_dir = tk.Button(f_frame, text = "Change", command = self.get_in_dir_path, width = 18, font = self.font_M, bg = self.color_btn, fg = self.color_text)
        btn_cout_dir = tk.Button(f_frame, text = "Change", command = self.get_out_dir_path, width = 18, font = self.font_M, bg = self.color_btn, fg = self.color_text)

        # Widget grid (define positions and look)
        f_frame.grid(row = 1, column = 0, columnspan = 2, sticky = "w")
        m_frame.grid(row = 6, column = 0, columnspan = 2, sticky = "w")

        lbl_file_setup.grid(row = 0, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_in_dir.grid(row = 1, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_in_name.grid(row = 2, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_out_dir.grid(row = 3, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_out_name.grid(row = 4, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        
        lbl_meas_setup.grid(row = 5, column = 0, sticky = "ew", padx = self.padx, pady = self.pady)
        lbl_inst_name.grid(row = 6, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_meas_num.grid(row = 7, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_start.grid(row = 8, column = 1, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_end.grid(row = 8, column = 2, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_channels.grid(row = 9, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_wait_time.grid(row = 10, column = 0, sticky = "w", padx = self.padx, pady = self.pady)
        lbl_units.grid(row = 10, column = 2, sticky = "w", padx = self.padx, pady = self.pady)
        
        self.ent_in_dir.grid(row = 1, column = 1, sticky = "ew", columnspan = 2, padx = self.padx, pady = self.pady)
        self.ent_in_name.grid(row = 2, column = 1, sticky = "ew", columnspan = 2, padx = self.padx, pady = self.pady)
        self.ent_out_dir.grid(row = 3, column = 1, sticky = "ew", columnspan = 2, padx = self.padx, pady = self.pady)
        self.ent_out_name.grid(row = 4, column = 1, sticky = "ew", columnspan = 2, padx = self.padx, pady = self.pady)

        self.ent_inst_name.grid(row = 6, sticky = "ew", column = 1)
        self.spi_meas_num.grid(row = 7, sticky = "ew", column = 1)
        self.spi_ch_start.grid(row = 9, sticky = "ew", column = 1)
        self.spi_ch_end.grid(row = 9, sticky = "ew", column = 2)
        self.spi_wtime.grid(row = 10, sticky = "ew", column = 1)

        btn_reset.grid(row = 0, column = 1, sticky = "e", padx = self.padx, pady = self.pady)
        btn_save_return.grid(row = 11, column = 1, sticky = "e", padx = self.padx, pady = self.pady)
        btn_cin_dir.grid(row = 1, column = 3, sticky = "ew", padx = self.padx, pady = self.pady)
        btn_cout_dir.grid(row = 3, column = 3, sticky = "ew", padx = self.padx, pady = self.pady)

    def save_and_return(self):
        """ Button function to save

        Saves all configured parameters and saves them into the rwfunc class
        and the base window labels
        """
        self.rwfunc.INPUT_DIR_PATH = self.ent_in_dir.get()
        self.rwfunc.INPUT_FILENAME = self.ent_in_name.get()
        self.rwfunc.INPUT_FILE_PATH = os.path.join(self.rwfunc.INPUT_DIR_PATH, self.rwfunc.INPUT_FILENAME)
        
        self.rwfunc.OUTPUT_DIR_PATH = self.ent_out_dir.get()
        self.rwfunc.OUTPUT_FILENAME = self.ent_out_name.get()
        self.rwfunc.OUTPUT_FILE_PATH = os.path.join(self.rwfunc.OUTPUT_DIR_PATH, self.rwfunc.OUTPUT_FILENAME)

        self.rwfunc.INSTRUMENT_NAME = self.ent_inst_name.get()
        self.rwfunc.MEAS_NUM = int(self.spi_meas_num.get())
        self.rwfunc.CHANNELS_START = int(self.spi_ch_start.get())
        self.rwfunc.CHANNELS_END = int(self.spi_ch_end.get())
        self.rwfunc.WAIT_TIME = float(self.spi_wtime.get())

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
        self.txt_console.insert(tk.INSERT, f"[INFO] New parameters saved.\n")

    def abort(self):
        """ Closes the program

        Also tries to close the files and instrument session
        """
        print("[INFO] Closing")
        try:
            # Try to correctly close files and session
            self.rwfunc.close_files()
            self.KeyDAQ.close_session()   
        except:
            # Only negative in fail:
            # instrument can be falsely detected as connected
            # next time (no response or connection, just display)
            print("[WARN] Error during shutdown.")
            pass
        # Exits the script
        print("[INFO] Done.")
        sys.exit()

    def start_program(self):
        """ Button function START

        Starting procedure of the program
        """
        # Remove the configure button
        self.btn_setup.grid_remove()

        self.txt_console.insert(tk.INSERT, f"[INFO] {curr_time()}: Started program.\n")

        # Pass the arguments to instrument class
        self.KeyDAQ = KeyDAQ(meas_num = self.rwfunc.MEAS_NUM,
                             wait_time = self.rwfunc.WAIT_TIME,
                             channels_start = self.rwfunc.CHANNELS_START,
                             channels_end = self.rwfunc.CHANNELS_END)
        self.KeyDAQ.init_inst()
        self.txt_console.insert(tk.INSERT, f"[INFO] Instrument initialized.\n")
        
        # Define thread and start
        self.main_loopTHREAD = threading.Thread(target = self.main_loop, daemon = True)
        self.main_loopTHREAD.start()

    def main_loop(self):
        """ Main loop 

        Wait for the original file to be created and then create new file.
        Copy heading and enter main loop.
        Main loop checks for new line, executes measurements and writes to new file.
        """
        print(f"[INFO] Start time: {curr_time()}")

        if self.rwfunc.check_f_exists(self.rwfunc.OUTPUT_FILE_PATH) == True:
            # If file exists stop execution
            return

        self.rwfunc.create_file(self.rwfunc.INPUT_FILE_PATH,
                                self.rwfunc.INPUT_FILENAME,
                                self.rwfunc.OUTPUT_FILE_PATH,
                                self.rwfunc.OUTPUT_FILENAME)
        self.txt_console.insert(tk.INSERT, f"[INFO] Files created.\n")

        self.rwfunc.write_heading()
        self.txt_console.insert(tk.INSERT, f"[INFO] Heading written.\n")

        try:
            TIMEOUT_MAX = 150
            timeout = 0
            while True:
                
                if timeout >= TIMEOUT_MAX:
                    print(f"[INFO] No change in last {TIMEOUT_MAX} checks ({TIMEOUT_MAX*self.rwfunc.WAIT_TIME} seconds)")
                    print(f"[INFO] End time: {curr_time()}")
                    self.rwfunc.close_files()
                    self.txt_console.insert(tk.INSERT, f"[INFO] No change in last {TIMEOUT_MAX} checks ({TIMEOUT_MAX*self.rwfunc.WAIT_TIME} seconds).\n")
                    self.txt_console.insert(tk.INSERT, f"[INFO] End time: {curr_time}\n")
                    break
                
                try:
                    self.rwfunc.read_lastline()

                    # Check if UI console is longer than specified
                    if int(float(self.txt_console.index("end"))) >= 30:
                        self.txt_console.delete(1.0, tk.END)

                    # If there is a new line execute measurement
                    if self.rwfunc.check_newline() == True:                        
                        self.KeyDAQ.acquire() # measurement
                        temps = self.KeyDAQ.process() # process temps.
                        self.rwfunc.write_line(temps) # write line

                        self.txt_console.insert(tk.INSERT, f"[INFO] {curr_time()}: Line {self.rwfunc.line_num} written. Temp: {temps}\n")
                        timeout = 0

                    # If there is no new line wait a bit and start the timeout timer
                    elif self.rwfunc.check_newline() == False:
                        time.sleep(self.rwfunc.WAIT_TIME)
                        timeout += 1
                except:
                    # Idealy the error is a one time thing
                    print("[ERROR] Error occured turing main loop. Retrying...")
                    self.txt_console.insert(tk.INSERT, f"[ERROR] Error occured turing main loop. Retrying...\n")
                    time.sleep(1)

        except KeyboardInterrupt:
            print("[INFO] Stopping...")
            pass

        #print(time.time()-start)
        
    def update_time(self):
        # Update time function call only once at beginning
        self.time_thread = threading.Thread(target = self.update_time_thread, daemon = True)
        self.time_thread.start()

    def update_time_thread(self):
        # Update time label every 0.1s
        try: 
            while True:
                self.lbl_clock.config(text = curr_time())
                time.sleep(0.1)
        except Exception as e:
            print(f"[WARN] Error with clock.\n{e}")
    
    def get_in_dir_path(self):
        self.subwin.destroy()
        directory = filedialog.askdirectory()

        # If you only open and immedialtely close the filedialog
        # to ask for directory it immediately sets variable as ""
        if directory == "":
            return
        else:
            self.rwfunc.INPUT_DIR_PATH = directory

        # Subwindow closes when using filedialog
        # Have to reopen it after
        self.create_subwindow()

    def get_out_dir_path(self):
        self.subwin.destroy()
        directory = filedialog.askdirectory()

        # If you only open and immedialtely close the filedialog
        # to ask for directory it immediately sets variable as ""
        if directory == "":
            return
        else:
            self.rwfunc.OUTPUT_DIR_PATH = directory

        # Subwindow closes when using filedialog
        # Have to reopen it after
        self.create_subwindow()

    def check_instrument(self):
        # Check instrument connection
        print("[INFO] Checking inst connection")
        checkInstT = threading.Thread(target=self.check_inst_thread, daemon=True)
        checkInstT.start()

    def check_inst_thread(self):
        # Checks response to *IDN?
        self.KeyDAQ = KeyDAQ()
        self.KeyDAQ.init_inst()
        response = self.KeyDAQ.check_response()
        self.txt_console.insert(tk.INSERT, f"[INFO] Instrument response to *IDN?: {response}\n")
        self.KeyDAQ.close_session()

if __name__ == "__main__":
    measUI = measUI(SIM=False)
    print("\n*---------------------------------------------------------------------*")
    print("Parameters:")

    dictionary = measUI.rwfunc.__dict__

    for key in dictionary:
        print(f"{key}:\t-->\t{dictionary[key]}")
