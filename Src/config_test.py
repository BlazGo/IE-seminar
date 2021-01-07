from configparser import ConfigParser

"""
Create the config.ini file
By running this code you can generate a new config file

Output:
    - config.ini file (with default program parameters)
"""

filename = "meas_setup.ini" # Output filename

config = ConfigParser()
config["DEFAULT"] = {"Input_dir_path"   : "C:/measurements",
                     "Input_filename"   : "read_file",
                     "Output_dir_path"  : "C:/measurements/modify",
                     "Output_filename"  : "write_file_T",
                     "Instrument"       : "Keysight DAQ970A",
                     "Meas_num"         : "11",
                     "Wait_time"        : "1",
                     "Channels_start"   : "101",
                     "Channels_end"     : "104"
                     }

config["FILE_SETUP"] = {"Input_dir_path" : "C:/measurements",
                        "Input_filename" : "read_file",
                        "Output_dir_path": "C:/measurements/modify",
                        "Output_filename": "write_file_T"
                        }

config["INSTRUMENT_SETUP"] = {  "Instrument"        : "Keysight DAQ970A",
                                "Meas_num"          : "11",
                                "Wait_time"         : "1",
                                "Channels_start"    : "101",
                                "Channels_end"      : "104"
                                }


with open(filename, "w") as configfile:
    config.write(configfile)