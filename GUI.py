import tkinter as tk

mainWindow = tk.Tk()
mainWindow.title("Vhodni podatki")
mainWindow.columnconfigure(0, minsize = 250)
mainWindow.rowconfigure([0,1], minsize = 100)

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

btn_change_in_dir = tk.Button(
    master = input_frame,
    text = "Spremeni",
    width = 10,
    height = 1
    )

btn_change_out_dir = tk.Button(
    master = output_frame,
    text = "Spremeni",
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

input_file_path = tk.StringVar()
ent_in_dir = tk.Entry(
    master = input_frame,
    textvariable = input_file_path,
    width = 60
    )

input_filename = tk.StringVar()
ent_in_name = tk.Entry(
    master = input_frame,
    textvariable = input_filename,
    width = 60
    )

output_file_path = tk.StringVar()
ent_out_dir = tk.Entry(
    master = output_frame,
    textvariable = output_file_path,
    width = 60
    )

output_filename = tk.StringVar()
ent_out_name = tk.Entry(
    master = output_frame,
    textvariable = output_filename,
    width = 60
    )

instrument = tk.StringVar()
ent_instrument = tk.Entry(
    master = other_frame,
    textvariable = instrument,
    width = 60
    )

ent_in_dir.insert(0, "default_in_dir_path_here")
ent_out_dir.insert(0, "default_out_dir_path_here")
ent_in_name.insert(0, "default_in_filename_here")
ent_out_name.insert(0, "default_out_filename_here")
ent_instrument.insert(0, "Keysight DAQ970A")

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

mainWindow.mainloop()

print(input_filename.get()) # this is how you get variables out 
















"""

menu = tk.Menu(mainWindow)
filemenu = tk.Menu(menu, tearoff = 0)
filemenu.add_command(label = "New")

filemenu.add_separator()
menu.add_cascade(label = "File", menu = filemenu)
mainWindow.config(menu = menu)

"""