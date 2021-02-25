import os
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from pyvisa import errors

# Custom libraries
from instlib import KeyDAQ
from rwlib import fileFunc


def do_nothing():
    # Placeholder for buttons
    print("Something")

def curr_time():
    """ Get current time.

    Returns:
    ----------
    Time : String
        Return time in string format 
        (hours:minutes:seconds day/month/year)
        
    """

    return datetime.now().strftime("%H:%M:%S %d/%m/%Y")


class measUI():
    """
    Class with UI definition 
    """

    # Time to timeout 
    TIMEOUT_MAX = 120*60  # [s]
    
    # Widget padding
    padx = 6
    pady = 3
    
    # Color definitions
    color_bg = "#212121"
    color_bg_s = "#1F2933"
    color_lbl = "#323F4B"
    color_disp = "#334E68"
    color_text = "#F5F7FA"
    color_btn = "#627D98"

    # Font definitions
    font_L = ('Leelawadee UI', 14)
    font_M = ('Leelawadee UI', 12)
    font_I = ('Consolas', 11)

    def __init__(self, master, simulation=False):
        """ Main window

        """
        # Simple simulation not implemented
        # Best solution to replace instrument calls with
        # random number generator manually
        self.SIM = simulation

        # Initiate class for files
        self.rwfunc = fileFunc()
        # Read config file and set parameters
        self.rwfunc.read_config()

        # Define UI basics
        self.root = master
        self.root.title("Merjenje temperature")
        #self.root.minsize(500, 400)
        # self.root.geometry("750x360")
        self.root.configure(bg=self.color_bg)

        f_frame = tk.Frame(self.root, bg=self.color_bg_s, relief="sunken")
        m_frame = tk.Frame(self.root, bg=self.color_bg_s, relief="sunken")

        # Descriptions display
        self.lbl_clock = tk.Label(self.root,  width=18, font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_console = tk.Label(self.root, text="Console", font=self.font_L, bg=self.color_lbl, fg=self.color_text)
        lbl_file_setup = tk.Label(f_frame, text="File setup", font=self.font_L, bg=self.color_lbl, fg=self.color_text)
        lbl_in_dir = tk.Label(f_frame, text="Input file folder path", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_in_name = tk.Label(f_frame, text="Input filename", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_out_dir = tk.Label(f_frame, text="Output file folder path", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_out_name = tk.Label(f_frame, text="Output filename", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_meas_setup = tk.Label(m_frame, text="Measurement setup", font=self.font_L, bg=self.color_lbl, fg=self.color_text)
        lbl_inst_name = tk.Label(m_frame, text="Instrument", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_meas_num = tk.Label(m_frame, text="Measurement number", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_channels = tk.Label(m_frame, text="Channels", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_chan_des = tk.Label(m_frame, text="Start:End", bg=self.color_bg, fg=self.color_text)
        lbl_wait_time = tk.Label(m_frame, text="Wait time", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_units = tk.Label(m_frame, text="[seconds]", bg=self.color_bg, fg=self.color_text)

        # Values display
        self.lbl_in_dirD = tk.Label(f_frame, text=self.rwfunc.INPUT_DIR_PATH, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")
        self.lbl_in_nameD = tk.Label(f_frame, text=self.rwfunc.INPUT_FILENAME, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")
        self.lbl_out_dirD = tk.Label(f_frame, text=self.rwfunc.OUTPUT_DIR_PATH, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")
        self.lbl_out_nameD = tk.Label(f_frame, text=self.rwfunc.OUTPUT_FILENAME, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")

        self.lbl_inst_nameD = tk.Label(m_frame, text=self.rwfunc.INSTRUMENT_NAME, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")
        self.lbl_meas_numD = tk.Label(m_frame, text=self.rwfunc.MEAS_NUM, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")

        channels = f"{self.rwfunc.CHANNELS_START}:{self.rwfunc.CHANNELS_END}"
        self.lbl_channelsD = tk.Label(m_frame, text=channels, font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")
        self.lbl_wait_timeD = tk.Label(m_frame, text=self.rwfunc.WAIT_TIME,font=self.font_I, bg=self.color_disp, fg=self.color_text, relief="sunken")

        # Buttons
        self.btn_setup = tk.Button(self.root, text="Configure", command=self.create_subwindow, font=self.font_M, width=18, bg=self.color_btn, fg=self.color_text)
        btn_start = tk.Button(self.root, text="Start", command=self.start_program, font=self.font_M, width=18, bg=self.color_btn, fg=self.color_text)
        btn_abort = tk.Button(self.root, text="Abort", command=self.abort, font=self.font_M, width=18, bg=self.color_btn, fg=self.color_text)
        self.btn_check_inst = tk.Button(m_frame, text="Check inst", command=self.check_inst, font=self.font_I, height=1, bg=self.color_btn, fg=self.color_text)
        self.btn_inst_scan = tk.Button(m_frame, text="Scan instruments", command=self.scan_for_inst, font=self.font_I, height=1, bg=self.color_btn, fg=self.color_text)

        self.txt_console = tk.Text(self.root, height=20, font=self.font_I, width=60)

        # Place widgets
        self.lbl_clock.grid(row=0, column=1, sticky="e", padx=self.padx, pady=self.pady)
        lbl_console.grid(row=0, column=2, sticky="ew", padx=self.padx, pady=self.pady)

        f_frame.grid(row=2, column=0, columnspan=2, sticky="new", padx=self.padx, pady=self.pady)
        m_frame.grid(row=7, column=0, columnspan=2, sticky="new", padx=self.padx, pady=self.pady)

        lbl_file_setup.grid(row=1, column=0, sticky="ew", padx=self.padx, pady=self.pady, columnspan=3)
        lbl_in_dir.grid(row=2, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_in_name.grid(row=3, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_out_dir.grid(row=4, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_out_name.grid(row=5, column=0, sticky="ew", padx=self.padx, pady=self.pady)

        lbl_meas_setup.grid(row=6, column=0, sticky="ew", padx=self.padx, pady=self.pady, columnspan=4)
        lbl_inst_name.grid(row=7, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_meas_num.grid(row=8, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_channels.grid(row=9, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_chan_des.grid(row=9, column=2, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_wait_time.grid(row=10, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_units.grid(row=10, column=2, sticky="ew", padx=self.padx, pady=self.pady)

        self.lbl_in_dirD.grid(row=2, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.lbl_in_nameD.grid(row=3, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.lbl_out_dirD.grid(row=4, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.lbl_out_nameD.grid(row=5, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.lbl_inst_nameD.grid(row=7, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        self.lbl_meas_numD.grid(row=8, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        self.lbl_channelsD.grid(row=9, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        self.lbl_wait_timeD.grid(row=10, column=1, sticky="ew", padx=self.padx, pady=self.pady)

        self.btn_setup.grid(row=0, column=0, sticky="w", padx=self.padx, pady=self.pady)
        btn_abort.grid(row=11, column=0, sticky="w", padx=self.padx, pady=self.pady)
        btn_start.grid(row=11, column=1, sticky="e", padx=self.padx, pady=self.pady)
        self.btn_check_inst.grid(row=7, column=2, sticky="ew", padx=self.padx, pady=self.pady)
        self.btn_inst_scan.grid(row=7, column=3, sticky="ew", padx=self.padx, pady=self.pady)


        self.txt_console.grid(row=1, column=2, sticky="news", padx=self.padx, pady=self.pady, rowspan=11)

        f_frame.columnconfigure(2, weight=1)
        m_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)

    def create_subwindow(self):
        """ Function that handles configuration subwindow

        """
        
        # Define window basic parameters
        self.subwin = tk.Toplevel(self.root, bg=self.color_bg)
        self.subwin.title("Nastavitve")
        #self.subwin.minsize(1252, 490)

        # self.subwin.geometry("700x350")

        f_frame = tk.Frame(self.subwin, bg=self.color_bg_s)
        m_frame = tk.Frame(self.subwin, bg=self.color_bg_s)

        # Label widgets
        lbl_file_setup = tk.Label(f_frame, text="File setup", font=self.font_L, bg=self.color_lbl, fg=self.color_text)
        lbl_in_dir = tk.Label(f_frame, text="Input file folder path", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_in_name = tk.Label(f_frame, text="Input filename", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_out_dir = tk.Label(f_frame, text="Output file folder path", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_out_name = tk.Label(f_frame, text="Output filename", font=self.font_M, bg=self.color_lbl, fg=self.color_text)

        lbl_meas_setup = tk.Label(m_frame, text="Measurement setup", font=self.font_L, bg=self.color_lbl, fg=self.color_text)
        lbl_inst_name = tk.Label(m_frame, text="Instrument", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_meas_num = tk.Label(m_frame, text="Measurement number", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_start = tk.Label(m_frame, text="Start", bg=self.color_lbl, fg=self.color_text)
        lbl_end = tk.Label(m_frame, text="End", bg=self.color_lbl, fg=self.color_text)
        lbl_channels = tk.Label(m_frame, text="Channels", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_wait_time = tk.Label(m_frame, text="Wait time", font=self.font_M, bg=self.color_lbl, fg=self.color_text)
        lbl_units = tk.Label(m_frame, text="[seconds]", bg=self.color_lbl, fg=self.color_text)

        # Entry widgets
        self.ent_in_dir = tk.Entry(f_frame, width=90, font=self.font_I)
        self.ent_in_name = tk.Entry(f_frame, width=90, font=self.font_I)
        self.ent_out_dir = tk.Entry(f_frame, width=90, font=self.font_I)
        self.ent_out_name = tk.Entry(f_frame, width=90, font=self.font_I)
        self.ent_inst_name = tk.Entry(m_frame, font=self.font_I)

        # Spinbox widgets
        meas_num_valid = tuple(range(1, 22, 2))
        self.spi_meas_num = tk.Spinbox(m_frame, values=meas_num_valid, font=self.font_I)
        self.spi_ch_start = tk.Spinbox(m_frame, from_=0, to=999, font=self.font_I)
        self.spi_ch_end = tk.Spinbox(m_frame, from_=0, to=999, font=self.font_I)
        self.spi_wtime = tk.Spinbox(m_frame, from_=0.1, to=20, increment=0.1, font=self.font_I)
 
        # Button widgets
        btn_cin_dir = tk.Button(f_frame, text="Change", command=self.get_in_dir_path, width=18, font=self.font_M, bg=self.color_btn, fg=self.color_text)
        btn_cout_dir = tk.Button(f_frame, text="Change", command=self.get_out_dir_path, width=18, font=self.font_M, bg=self.color_btn, fg=self.color_text)
        btn_reset = tk.Button(self.subwin, text="Reset", command=self.reset_to_default, width=18, font=self.font_M, bg=self.color_btn, fg=self.color_text)
        btn_save_return = tk.Button(self.subwin, text="Save and return", command=self.save_and_return, width=18, font=self.font_M, bg=self.color_btn, fg=self.color_text)

        # Widget grid (define positions and look)
        f_frame.grid(row=1, column=0, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        m_frame.grid(row=6, column=0, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)

        lbl_file_setup.grid(row=0, column=0, sticky="ew", padx=self.padx, pady=self.pady, columnspan=3)
        lbl_in_dir.grid(row=1, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_in_name.grid(row=2, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_out_dir.grid(row=3, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_out_name.grid(row=4, column=0, sticky="ew", padx=self.padx, pady=self.pady)

        lbl_meas_setup.grid(row=5, column=0, columnspan=3, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_inst_name.grid(row=6, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_meas_num.grid(row=7, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_start.grid(row=8, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_end.grid(row=8, column=2, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_channels.grid(row=9, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_wait_time.grid(row=10, column=0, sticky="ew", padx=self.padx, pady=self.pady)
        lbl_units.grid(row=10, column=2, sticky="ew", padx=self.padx, pady=self.pady)

        self.ent_in_dir.grid(row=1, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.ent_in_name.grid(row=2, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.ent_out_dir.grid(row=3, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)
        self.ent_out_name.grid(row=4, column=1, sticky="ew", padx=self.padx, pady=self.pady, columnspan=2)

        self.ent_inst_name.grid(row=6, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        self.spi_meas_num.grid(row=7, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        self.spi_ch_start.grid(row=9, column=1, sticky="ew", padx=self.padx, pady=self.pady)
        self.spi_ch_end.grid(row=9, column=2, sticky="ew", padx=self.padx, pady=self.pady)
        self.spi_wtime.grid(row=10, column=1, sticky="ew", padx=self.padx, pady=self.pady)

        btn_save_return.grid(row=11, column=1, sticky="e", padx=self.padx, pady=self.pady)
        btn_cin_dir.grid(row=1, column=3, sticky="ew", padx=self.padx, pady=self.pady)
        btn_reset.grid(row=11, column=0, sticky="w", padx=self.padx, pady=self.pady)
        btn_cout_dir.grid(row=3, column=3, sticky="ew", padx=self.padx, pady=self.pady)

        # Insert values into widgets
        self.spi_meas_num.delete(0, tk.END)
        self.spi_ch_start.delete(0, tk.END)
        self.spi_ch_end.delete(0, tk.END)
        self.spi_wtime.delete(0, tk.END)
        self.ent_in_dir.insert(0, self.rwfunc.INPUT_DIR_PATH)
        self.ent_in_name.insert(0, self.rwfunc.INPUT_FILENAME)
        self.ent_out_dir.insert(0, self.rwfunc.OUTPUT_DIR_PATH)
        self.ent_out_name.insert(0, self.rwfunc.OUTPUT_FILENAME)
        self.ent_inst_name.insert(0, self.rwfunc.INSTRUMENT_NAME)
        self.spi_meas_num.insert(0, self.rwfunc.MEAS_NUM)
        self.spi_ch_start.insert(0, self.rwfunc.CHANNELS_START)
        self.spi_ch_end.insert(0, self.rwfunc.CHANNELS_END)
        self.spi_wtime.insert(0, self.rwfunc.WAIT_TIME)

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

        self.lbl_in_dirD.config(text=self.rwfunc.INPUT_DIR_PATH)
        self.lbl_in_nameD.config(text=self.rwfunc.INPUT_FILENAME)
        self.lbl_out_dirD.config(text=self.rwfunc.OUTPUT_DIR_PATH)
        self.lbl_out_nameD.config(text=self.rwfunc.OUTPUT_FILENAME)
        self.lbl_inst_nameD.config(text=self.rwfunc.INSTRUMENT_NAME)
        self.lbl_meas_numD.config(text=self.rwfunc.MEAS_NUM)
        channels = f"{self.rwfunc.CHANNELS_START}:{self.rwfunc.CHANNELS_END}"
        self.lbl_channelsD.config(text=channels)
        self.lbl_wait_timeD.config(text=self.rwfunc.WAIT_TIME)

        # Close the subwindow
        self.subwin.destroy()
        self.txt_console.insert(tk.INSERT, f"[INFO] New parameters saved.\n")

    def reset_to_default(self):
        """ Button function resets parameters to default values.
        Reads the configuration file again and saves parameters.
        
        """

        self.rwfunc.read_config()

        # First delete the widget data if not it just adds
        self.ent_in_dir.delete(0, tk.END)
        self.ent_in_name.delete(0, tk.END)
        self.ent_out_dir.delete(0, tk.END)
        self.ent_out_name.delete(0, tk.END)
        self.ent_inst_name.delete(0, tk.END)
        self.spi_meas_num.delete(0, tk.END)
        self.spi_ch_start.delete(0, tk.END)
        self.spi_ch_end.delete(0, tk.END)
        self.spi_wtime.delete(0, tk.END)

        # Insert new data
        self.ent_in_dir.insert(0, self.rwfunc.INPUT_DIR_PATH)
        self.ent_in_name.insert(0, self.rwfunc.INPUT_FILENAME)
        self.ent_out_dir.insert(0, self.rwfunc.OUTPUT_DIR_PATH)
        self.ent_out_name.insert(0, self.rwfunc.OUTPUT_FILENAME)
        self.ent_inst_name.insert(0, self.rwfunc.INSTRUMENT_NAME)
        self.spi_meas_num.insert(0, self.rwfunc.MEAS_NUM)
        self.spi_ch_start.insert(0, self.rwfunc.CHANNELS_START)
        self.spi_ch_end.insert(0, self.rwfunc.CHANNELS_END)
        self.spi_wtime.insert(0, self.rwfunc.WAIT_TIME)

    def abort(self):
        """ Closes the program

        Also tries to close the files and instrument session
        
        """

        print("[INFO] Closing")

        # Try to correctly close files and session
        try:
            self.rwfunc.close_files()
        except AttributeError as e:
            print(f"[WARN] AttributeError during file close: No file to close. {e}")

        try:
            self.KeyDAQ.close_session()
        except AttributeError as e:
            # Only negative in fail:
            # instrument can be falsely detected as connected
            # next time (no response or connection, just display)
            # No error if you want to normally connect to it again,
            # if of course it is present.
            print(f"[WARN] AttributeError during inst. session close: {e} ")

        print("[INFO] Done.")
        sys.exit()

    def start_program(self):
        """ Button function START

        Start the main program thread.
        
        """

        self.main_loopTHREAD = threading.Thread(target=self.main_loop, daemon=True)
        self.main_loopTHREAD.start()

    def main_loop(self):
        """ Main program
        Initialize instrument, copy heading remove buttons.
        Main loop checks for new line, executes measurements and writes to new file.

        """

        self.KeyDAQ = KeyDAQ(meas_num=self.rwfunc.MEAS_NUM,
                             channels_start=self.rwfunc.CHANNELS_START,
                             channels_end=self.rwfunc.CHANNELS_END,
                             tolerance=self.rwfunc.TOLERANCE,
                             simulation=self.SIM)

        try:
            self.KeyDAQ.init_inst(resource=self.rwfunc.INSTRUMENT_ADDRESS)
        except errors.VisaIOError:
            message = f"[ERROR] Instrument may not be present. Cannot continue."
            print(message)  
            self.txt_console.insert(tk.INSERT, message + "\n")
            raise

        message = f"[INFO] Instrument initialized."
        print(message)  
        self.txt_console.insert(tk.INSERT, message + "\n")

        try:
            self.rwfunc.create_file(self.rwfunc.INPUT_FILE_PATH,
                                self.rwfunc.INPUT_FILENAME,
                                self.rwfunc.OUTPUT_FILE_PATH,
                                self.rwfunc.OUTPUT_FILENAME)
        except FileExistsError:
            message = f"[ERROR] Files already exists. Change the name of the output file."
            print(message)
            self.txt_console.insert(tk.INSERT, message + "\n")
            raise

        message = f"[INFO] Files created."
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")

        self.rwfunc.write_heading()

        message = f"[INFO] Heading written."
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")

        # Remove the unnecessary buttons just in case
        self.btn_setup.grid_remove()
        self.btn_inst_scan.grid_remove()
        self.btn_check_inst.grid_remove()
        
        message = f"[INFO] {curr_time()}: Started program."
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")

        #timeout_timer = time.time()
        while True:
            try:
                # Check if UI console is longer than specified
                if int(float(self.txt_console.index("end"))) >= 30:
                    self.txt_console.delete(1.0, tk.END)

                """
                if time.time() - timeout_timer >= self.TIMEOUT_MAX:
                    message = f"[INFO] {curr_time()}: Reached timeout time.\n"
                    print(message)
                    self.txt_console.insert(tk.INSERT, message)
                    # If timeout is reached exit the main loop
                    break
                """

                start = time.time()

                # If there is a new line execute measurement
                if self.rwfunc.check_newline() == True:
                    # measurement
                    measurements = self.KeyDAQ.get_measurements()
                    # write line
                    self.rwfunc.write_new_line(self.rwfunc.last_line, measurements)

                    measurements = [round(num, 1) for num in measurements]
                    message = f"[INFO] {curr_time()}: Line {self.rwfunc.line_num} written. Temp: {measurements}"
                    print(message)
                    self.txt_console.insert(tk.INSERT, message + "\n")

                    # reset the timeout timer
                    # timeout_timer = time.time()
                    meas_time = (time.time() - start)*1e-3 # Get seconds
                    time_remaining = self.rwfunc.WAIT_TIME - meas_time

                    if time_remaining <= 0:
                        time_remaining = 0
                    if time_remaining > self.rwfunc.WAIT_TIME:
                        time_remaining = self.rwfunc.WAIT_TIME

                    time.sleep(time_remaining)

                # If there is no new line wait a bit and start the timeout timer
                elif self.rwfunc.check_newline() == False:
                    time.sleep(self.rwfunc.WAIT_TIME)

            except Exception as e:
                # If there was an error in main loop it was programming mistake.
                # This is probably useless.
                message = f"[ERROR] Error occured turing main loop. Retrying...\n Error {e}"
                print(message)
                self.txt_console.insert(tk.INSERT, message + "\n")
                time.sleep(self.rwfunc.WAIT_TIME/2)
                # Maybe put here .after() to restart the main loop
                # probably only while loop?
                raise

    def update_time(self):
        """ Function to start the update time 
        thread in the background.

        """        
        
        self.timeThread = threading.Thread(target=self.update_time_thread, daemon=True)
        self.timeThread.start()

    def update_time_thread(self):
        """ Function to update time.

        """
       
        try:
             while True:
                self.lbl_clock.config(text=curr_time())
                time.sleep(0.1)
        except Exception as e:
            print(f"[WARN] Error with clock.\n{e}")
            self.txt_console.insert(tk.INSERT, f"[WARN] Error with clock.\n{e}")    

    def get_in_dir_path(self):
        """ Button function to get outpit file directory

        """

        self.subwin.destroy()
        directory = filedialog.askdirectory()

        # If you only open and immedialtely close the filedialog
        # to ask for directory it immediately sets variable as ""
        if directory != "":
            self.rwfunc.INPUT_DIR_PATH = directory
        
        # Subwindow closes when using filedialog
        # Have to reopen it after
        self.create_subwindow()

    def get_out_dir_path(self):
        """ Button function to get outpit file directory
        
        """

        self.subwin.destroy()
        directory = filedialog.askdirectory()

        # If you only open and immedialtely close the filedialog
        # to ask for directory it immediately sets variable as ""
        if directory != "":
            self.rwfunc.OUTPUT_DIR_PATH = directory

        # Subwindow closes when using filedialog
        # Have to reopen it after
        self.create_subwindow()

    def check_inst(self):
        """ Checks connection with instrument

        Parameters:
        ----------
        config_filename : configuration filename (optional default already set)

        """

        message = "[INFO] Checking inst connection"
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")

        checkInstThread = threading.Thread(target=self.check_inst_thread, daemon=True)
        checkInstThread.start()

    def check_inst_thread(self):
        """ Prints out the instrument response to *IDN?

        """
        self.KeyDAQ_test = KeyDAQ(simulation=self.SIM)

        try:
            self.KeyDAQ_test.init_inst()
        except errors.VisaIOError:
            message = f"[ERROR] Insufficient location information or the requested device or resource is not present in the system.\n"
            print(message)  
            self.txt_console.insert(tk.INSERT, message)
            raise
        except errors.InvalidSession:
            message = f"[ERROR] Invalid session handle. The resource might be closed.\n"
            print(message)  
            self.txt_console.insert(tk.INSERT, message)
            raise

        response, meas = self.KeyDAQ_test.check_response()

        message = f"[INFO] Instrument response to *IDN?: {response}"
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")

        message = f"[INFO] Test measurement: {meas}"
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")
        
        try:
            for element in meas:
                # What is the expected temperature?
                if element >= 200 or element <= -1:
                    raise ValueError("[WARN] Some channels may not be configured correctly")
        finally:
            self.KeyDAQ_test.close_session()

    def scan_for_inst(self):
        """ Returns a list of found resources to choose from

        """
        self.KeyDAQ_test = KeyDAQ(simulation=self.SIM)
        inst_list = self.KeyDAQ_test.scan_resources()
        message = f"[INFO] Instruments: {inst_list}"
        print(message)
        self.txt_console.insert(tk.INSERT, message + "\n")
        try: 
            self.KeyDAQ_test.close_session()
        except AttributeError:
            # No instrument initialized yet so it raises an attribute erroe
            # since it cant close it.
            pass

if __name__ == "__main__":
    
    root = tk.Tk()
    measUI = measUI(root, simulation=False)
    
    # Start clock update
    measUI.update_time()
    # Start main UI loop
    root.mainloop()

    print("\n*---------------------------------------------------------------------*")
    print("Parameters:")

    dictionary = measUI.rwfunc.__dict__

    for key in dictionary:
        print(f"{key}:\t-->\t{dictionary[key]}")

    print("\n*---------------------------------------------------------------------*")
