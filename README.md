# IE-seminar
School-firm collaboration project

- GUI: script with UI window with tkinter package
- Main: main script which creates a new file and reads the specified file
- test_data_creator: simulates the creation of the specified file (writing line by line in intervals)
- visaRes: custom library to set up and communicate with instrument
- default_config: text file which includes default parameters for the program

To start program run script GUI.py
'python GUI.py
An UI should open where you can check measurement parameters. If you want to change press the configure button.

When started a window will open with default parameters.
To change these press configure and change what is necessary and press save and return.
To check if the program can communicate with the instrument press the check instrument button. Currently hard coded the instrument address. No way to change in the GUI. It selects the first connected instrument.
When all is ready press the start button. The program shouls start if the instument is properly connected and initialized, the file to create has a unique name and the file to read is properly defined. Program only starts (by itself) when the file to read is created. 
There is a timeout implemented that if in 50 checks there is no difference in the file it will stop.
If anything goes wrong during operation recommended action is to start everything normally again and define a new output file. It should start copying and measuring from the (current) last line.