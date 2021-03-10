import configparser
import os

"""
Create the config.ini file
By running this code you can generate a new config file

Returns:
----------
config.ini : file (with default program parameters)

"""

filename = "config.ini"   # Output filename
script_path = os.path.dirname(os.path.realpath(__file__))  # Current script location

config = configparser.ConfigParser()

config["FILE_SETUP"] = {"Input_dir_path"    : str(script_path),
                        "Input_filename"    : "input_file.txt",
                        "Output_dir_path"   : str(script_path),
                        "Output_filename"   : "output_file.txt"
                        }

config["INSTRUMENT_SETUP"] = {  "Instrument"        : "Keysight DAQ970A",
                                "Instrument_address": "USB0::0x2A8D::0x5001::MY58004219::0::INSTR",
                                "Thermocouple_type" : "J",
                                "Channels_start"    : "101",
                                "Channels_end"      : "105"
                                }

config["MEASUREMENT_SETUP"] = { "Meas_num"      : "9",
                                "Tolerance"     : "1",
                                "Wait_time"     : "2.0",
                                "Async_temp"    : "True"
                                }

config["DEFAULT"] = {"Input_dir_path"       : "C:/measurements",
                     "Input_filename"       : "input.txt",
                     "Output_dir_path"      : "C:/measurements/modify",
                     "Output_filename"      : "output.txt",
                     "Instrument"           : "Keysight DAQ970A",
                     "Instrument_address"   : "USB0::0x2A8D::0x5001::MY58004219::0::INSTR",
                     "Thermocouple_type"    : "J",
                     "Meas_num"             : "11",
                     "Wait_time"            : "1",
                     "Channels_start"       : "101",
                     "Channels_end"         : "105",
                     "Async_temp"           : "False"
                     }

with open(filename, "w") as configfile:
    config.write(configfile)