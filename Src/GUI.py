import tkinter as tk
from tkinter import filedialog

def do_nothing():
    print("not implemented")

class simpleUI():

    def __init__(self, input_parameters = ""):
            
        # Setup #
        #------------------------------#

        # Widget colors
        self.fg_color = "#0B3948"
        self.bg_color = "#ACB0BD"
        self.bt_color = "#EAEDED"
        self.lbl_color = "#D0CDD7"
        self.ent_color = "#D9DBF1"

        # Main window setup
        mainWindow = tk.Tk()
        mainWindow.title("Vhodni podatki")
        mainWindow.columnconfigure(0, minsize = 250)
        mainWindow.rowconfigure([0,1], minsize = 100)

        # Top menu setup
        menubar = tk.Menu(mainWindow)
        helpmenu = tk.Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = "How to use", command = do_nothing)
        menubar.add_cascade(label = "Help", menu = helpmenu)
        
        mainWindow.config(bg = self.bg_color, menu = menubar)

        # Save input parameters from config
        self.input_parameters = input_parameters

        self.input_dir_path = "default in dir path"
        self.input_filename = tk.StringVar()
        self.input_filename.set("default in filename")
        self.output_dir_path = "default out dir path"
        self.output_filename = tk.StringVar()
        self.output_filename.set("default out filename")
        self.instrument = "Keysight DAQ970A"
        self.meas_num = 11
        self.meas_time = 1

        # Frames setup
        input_frame = tk.Frame(bg = self.bg_color, relief = tk.SUNKEN, borderwidth = 3)
        output_frame = tk.Frame(bg = self.bg_color,relief = tk.SUNKEN, borderwidth = 3)
        other_frame = tk.Frame(bg = self.bg_color)
        input_frame.pack(padx = 10,pady = 10,)
        output_frame.pack(padx = 10, pady = 10)
        other_frame.pack(padx = 10, pady = 10)

    
        # Text #
        #------------------------------#

        lbl_heading = tk.Label(
            text = "Preverite vhodne podatke",
            #foreground = "#FFC300",
            #background = "#581845",
            width = 100,
            height = 5
            )
        #lbl_heading.pack()

        lbl_in_dir = tk.Label(
            master = input_frame,
            text = "Mesto vhodne datoteke",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )

        lbl_in_name = tk.Label(
            master = input_frame,
            text = "Ime vhodne datoteke",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )

        lbl_out_dir = tk.Label(
            master = output_frame,
            text = "Mesto izhodne datoteke",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )
            
        lbl_out_name = tk.Label(
            master = output_frame,
            text = "Ime izhodne datoteke",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )

        lbl_instrument = tk.Label(
            master = other_frame,
            text = "Uporabljen instrument",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )

        lbl_meas_num = tk.Label(
            master = other_frame,
            text = "Stevilo zajemov",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )

        lbl_meas_time = tk.Label(
            master = other_frame,
            text = "Cas meritve",
            bg = self.lbl_color,
            width = 25,
            height = 1
            )


        # Buttons functions #
        #------------------------------#

        def get_in_dir_path():
            temp = self.input_dir_path
            self.input_dir_path = filedialog.askdirectory()

            # If you only open and immedialtely close the filedialog
            # to ask for directory it immediately sets variable as ""
            if self.input_dir_path == "":
                self.input_dir_path = temp
            else:
                ent_in_dir.delete(0, "end")
                ent_in_dir.insert(0, self.input_dir_path)

        def get_out_dir_path():
            temp = self.output_dir_path
            self.output_dir_path = filedialog.askdirectory()

            if self.output_dir_path == "":
                self.output_dir_path = temp
            else:
                ent_out_dir.delete(0, "end")
                ent_out_dir.insert(0, self.output_dir_path)

        def abort_program():
            print("Execution aborted.")
            exit()

        def close_continue():
            print("Data recorded. Continuing...")
            mainWindow.destroy()


        # Buttons #
        #------------------------------#

        btn_change_in_dir = tk.Button(
            master = input_frame,
            text = "Spremeni",
            command = get_in_dir_path,
            bg = self.bt_color,
            width = 10,
            height = 1
            )

        btn_change_out_dir = tk.Button(
            master = output_frame,
            text = "Spremeni",
            command = get_out_dir_path,
            bg = self.bt_color,
            width = 10,
            height = 1
            )

        btn_save_and_continue = tk.Button(
            master = other_frame,
            text = "Nadaljuj",
            command = close_continue,
            bg = self.bt_color,
            width = 15,
            height = 2
            )

        btn_abort_program = tk.Button(
            master = other_frame,
            text = "Prekliči",
            command = abort_program,
            bg = self.bt_color,
            width = 15,
            height = 2
            )

        # Input #
        #------------------------------#

        ent_in_dir = tk.Entry(
            master = input_frame,
            textvariable = self.input_dir_path,
            bg = self.ent_color,
            width = 60
            )

        ent_in_name = tk.Entry(
            master = input_frame,
            textvariable = self.input_filename,
            bg = self.ent_color,
            width = 60
            )

        ent_out_dir = tk.Entry(
            master = output_frame,
            textvariable = self.output_dir_path,
            bg = self.ent_color,
            width = 60
            )

        ent_out_name = tk.Entry(
            master = output_frame,
            textvariable = self.output_filename,
            bg = self.ent_color,
            width = 60
            )

        ent_instrument = tk.Entry(
            master = other_frame,
            textvariable = self.instrument,
            bg = self.ent_color,
            width = 60
            )
        
        ent_meas_num = tk.Entry(
            master = other_frame,
            textvariable = self.meas_num,
            bg = self.ent_color,
            width = 60
            )
        
        ent_meas_time = tk.Entry(
            master = other_frame,
            textvariable = self.meas_time,
            bg = self.ent_color,
            width = 60
            )


        # Set default #
        #------------------------------#
        ent_in_dir.insert(0, self.input_dir_path)
        ent_out_dir.insert(0, self.output_dir_path)
        ent_instrument.insert(0, self.instrument)
        ent_meas_num.insert(0, self.meas_num)
        ent_meas_time.insert(0, self.meas_time)

        # Draw #
        #------------------------------#

        lbl_in_dir.grid(row = 0, column = 0, padx=5, pady=5, sticky = "w")
        ent_in_dir.grid(row = 0, column = 1, padx=5, pady=5)
        btn_change_in_dir.grid(row = 0, column = 2, padx=5, pady=5)
        lbl_in_name.grid(row = 1, column = 0, padx=5, pady=5)
        ent_in_name.grid(row = 1, column = 1, padx=5, pady=5)

        lbl_out_dir.grid(row = 0, column = 0, padx=5, pady=5, sticky = "w")
        ent_out_dir.grid(row = 0, column = 1, padx=5, pady=5)
        btn_change_out_dir.grid(row = 0, column = 2, padx=5, pady=5)
        lbl_out_name.grid(row = 1, column = 0, padx=5, pady=5)
        ent_out_name.grid(row = 1, column = 1, padx=5, pady=5)

        lbl_instrument.grid(row = 0, column = 0, padx=5, pady=5)
        ent_instrument.grid(row = 0, column = 1, padx=5, pady=5)
        lbl_meas_num.grid(row = 1, column = 0, padx=5, pady=5)
        ent_meas_num.grid(row = 1, column = 1, padx=5, pady=5)
        lbl_meas_time.grid(row = 2, column = 0, padx=5, pady=5)
        ent_meas_time.grid(row = 2, column = 1, padx=5, pady=5)
    
        btn_abort_program.grid(row = 3, column = 0, padx=5, pady=5)
        btn_save_and_continue.grid(row = 3, column = 2, padx=5, pady=5)

        # Main loop #
        #------------------------------#
        mainWindow.mainloop()


        # Pack output parameters #
        #------------------------------#
        self.output_parameter_list = {
            "Input dir path"    : self.input_dir_path,
            "Input filename"    : self.input_filename.get(),
            "Ouput dir path"    : self.output_dir_path,
            "Output filename"   : self.output_filename.get(),
            "Instrument"        : self.instrument,
            "Meas num"          : self.meas_num,
            "Meas time"         : self.meas_time
            }

if __name__ == "__main__":

    UI = simpleUI()

    print("\nOutput parameters:")
    print("---------------------------------------")
    for item in UI.output_parameter_list:
        if item == "Instrument":
            print("{}:\t\t\t{}".format(item, UI.output_parameter_list.get(item)))
        else:
            print("{}:\t\t{}".format(item, UI.output_parameter_list.get(item)))
    print("---------------------------------------")

