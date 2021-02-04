from configparser import ConfigParser

"""
Create the config.ini file
By running this code you can generate a new config file

Output:
    - config.ini file (with default program parameters)
"""

filename = "config.ini" # Output filename

config = ConfigParser()
# Default (could be removed)
config["DEFAULT"] = {"Input_dir_path"   : "C:/measurements",
                     "Input_filename"   : "input.txt",
                     "Output_dir_path"  : "C:/measurements/modify",
                     "Output_filename"  : "output.txt",
                     "Instrument"       : "Keysight DAQ970A",
                     "Meas_num"         : "11",
                     "Wait_time"        : "1",
                     "Channels_start"   : "101",
                     "Channels_end"     : "105"
                     }

config["FILE_SETUP"] = {"Input_dir_path" : "C:/Users/dd/Desktop/Fe/SRM/IE-seminar/",
                        "Input_filename" : "input_file.txt",
                        "Output_dir_path": "C:/Users/dd/Desktop/Fe/SRM/IE-seminar/",
                        "Output_filename": "output_file.txt"
                        }

config["INSTRUMENT_SETUP"] = {  "Instrument"        : "Keysight DAQ970A",
                                "Meas_num"          : "9",
                                "Wait_time"         : "2.5",
                                "Channels_start"    : "101",
                                "Channels_end"      : "105"
                                }

with open(filename, "w") as configfile:
    config.write(configfile)