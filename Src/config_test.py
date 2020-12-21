import configparser

"""
Create the config.ini file
In this code you can generate a new config file.

Output:
    - config.ini file (with default program parameters)
"""

config = configparser.ConfigParser()
config["DEFAULT"] = {"Input_dir_path" : "C:/measurements",
                     "Input_filename" : "read_file",
                     "Output_dir_path": "C:/measurements/modify",
                     "Output_filename": "write_file_T",
                     "Instrument"     : "Keysight DAQ970A",
                     "Num_meas"  : "11",
                     "Time_meas" : "1"
                     }


config["FILE_SETUP"] = {"Input_dir_path" : "C:/measurements",
                        "Input_filename" : "read_file",
                        "Output_dir_path": "C:/measurements/modify",
                        "Output_filename": "write_file_T"
                        }

config["INSTRUMENT_SETUP"] = {  "Instrument": "Keysight DAQ970A",
                                "Meas_num"  : "10",
                                "Meas_time" : "1"
                                }

with open("meas_setup.ini", "w") as configfile:
    config.write(configfile)