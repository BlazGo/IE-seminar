import tkinter as tk
from tkinter import filedialog


class simpleUI():

    def __init__(self, input_parameters = ""):
            
        # Setup #
        #------------------------------#

        mainWindow = tk.Tk()
        mainWindow.title("Vhodni podatki")
        mainWindow.columnconfigure(0, minsize = 250)
        mainWindow.rowconfigure([0,1], minsize = 100)

        self.input_parameters = input_parameters

        self.input_dir_path = "default in dir path"
        self.input_filename = tk.StringVar()
        self.input_filename.set("default in filename")
        self.output_dir_path = "default out dir path"
        self.output_filename = tk.StringVar()
        self.output_filename.set("default out filename")
        self.instrument = "Keysight DAQ970A"

        input_frame = tk.Frame(relief = tk.SUNKEN, borderwidth = 3)
        output_frame = tk.Frame(relief = tk.SUNKEN, borderwidth = 3)
        other_frame = tk.Frame()
        input_frame.pack(padx = 10, pady = 10)
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
            width = 25,
            height = 1
            )

        lbl_in_name = tk.Label(
            master = input_frame,
            text = "Ime vhodne datoteke",
            width = 25,
            height = 1
            )

        lbl_out_dir = tk.Label(
            master = output_frame,
            text = "Mesto izhodne datoteke",
            width = 25,
            height = 1
            )
            
        lbl_out_name = tk.Label(
            master = output_frame,
            text = "Ime izhodne datoteke",
            width = 25,
            height = 1
            )

        lbl_instrument = tk.Label(
            master = other_frame,
            text = "Uporabljen instrument",
            width = 25,
            height = 1
            )


        # Buttons #
        #------------------------------#

        def get_in_dir_path():
            temp = self.input_dir_path
            self.input_dir_path = filedialog.askdirectory()

            # If you only open and immedialtely close the filedialog
            # to ask for directory it immediately sets variable as ""
            if self.input_dir_path == "":
                self.input_dir_path = temp
            else:
                ent_in_dir.insert(0, self.input_dir_path)

        def get_out_dir_path():
            temp = self.input_dir_path
            self.output_dir_path = filedialog.askdirectory()

            if self.output_dir_path == "":
                self.output_dir_path = temp
            else:
                ent_in_dir.insert(0, self.output_dir_path)

        btn_change_in_dir = tk.Button(
            master = input_frame,
            text = "Spremeni",
            command = get_in_dir_path,
            width = 10,
            height = 1
            )

        btn_change_out_dir = tk.Button(
            master = output_frame,
            text = "Spremeni",
            command = get_out_dir_path,
            width = 10,
            height = 1
            )

        btn_save_and_continue = tk.Button(
            master = other_frame,
            text = "Shrani in nadaljuj",
            width = 15,
            height = 2
            )


        # Input #
        #------------------------------#

        ent_in_dir = tk.Entry(
            master = input_frame,
            textvariable = self.input_dir_path,
            width = 60
            )

        ent_in_name = tk.Entry(
            master = input_frame,
            textvariable = self.input_filename,
            width = 60
            )

        ent_out_dir = tk.Entry(
            master = output_frame,
            textvariable = self.output_dir_path,
            width = 60
            )

        ent_out_name = tk.Entry(
            master = output_frame,
            textvariable = self.output_filename,
            width = 60
            )

        ent_instrument = tk.Entry(
            master = other_frame,
            textvariable = self.instrument,
            width = 60
            )


        # Set default #
        #------------------------------#
        ent_in_dir.insert(0, self.input_dir_path)
        #ent_in_name.insert(0, self.input_filename.get())
        ent_out_dir.insert(0, self.output_dir_path)
        #ent_out_name.insert(0, self.output_filename.get())
        ent_instrument.insert(0, self.instrument)


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
        btn_save_and_continue.grid(row = 2, column = 2, padx=5, pady=5)


        # Main loop #
        #------------------------------#
        mainWindow.mainloop()


        # Pack output parameters #
        #------------------------------#
        self.output_parameter_list = {
            "Input folder path" : self.input_dir_path,
            "Input file name"    : self.input_filename.get(),
            "Ouput folder path" : self.output_dir_path,
            "Output file name"   : self.output_filename.get(),
            "Instrument"        : self.instrument
            }

if __name__ == "__main__":

    UI = simpleUI()

    print("\nOutput parameters:\n---------------------------------------")
    for item in UI.output_parameter_list:
        if item == "Instrument":
            print("{}:\t\t\t{}".format(item, UI.output_parameter_list.get(item)))
        else:
            print("{}:\t\t{}".format(item, UI.output_parameter_list.get(item)))

    print("---------------------------------------")

