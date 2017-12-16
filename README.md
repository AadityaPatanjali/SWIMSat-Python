# SWIMSat-Python

## Dependencies

Install the following dependencies:

- numpy
- OpenCV 
- matplotlib
- Cython
- scipy 
- statsmodels

```
sudo pip install numpy opencv-python
sudo pip install --upgrade matplotlib
sudo pip install cython
sudo pip install scipy statsmodels```

Note: If any of the above libraries don't get installed on Windows, use [Gohlke's Unofficial Windows Binaries for Python Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

## Instructions to run

- Install git and run 
```
git clone https://github.com/AadityaPatanjali/SWIMSat-Python.git
```
- Change directory to SWIMSat-Python 
```
cd SWIMSat-Python
```
- Connect the PhantomX Pincher and the webcam to the computer. 
- Find out the port to which the robotic arm is connected.
  - Eg. /dev/ttyUSB0 for linux systems, COM3 for Windows, /dev/ttyACM0 for some Macs
  - If the port is not known, run 
```
python IntegratedVisionController.py
``` to find out the port.
- Own the port by using Eg. 
```
sudo chown <username> /dev/ttyUSB0``` or ```sudo chmod +x /dev/ttyUSB0```
- Run ```python IntegratedVisionController.py <port>``` replacing <port> by the appropriate port.
- A question will pop up to move to the Home Position. If the answer is no, you can reset the Home position (Use Ctrl + C to select a home position), automatically saving the new position.
- You will see two windows, Frame and Mask.
- Threshold of objects can be set by running the range_detector by using 
```
python range_detector.py --filter HSV --webcam
``` or by modifying the 'Image Threshold' file. Open it in any text editor, but don't modify the syntax. Syntax is 
```
[H_upper,S_upper,V_upper,H_lower,S_lower,V_lower]
``` where H, S and, V stand for Hue, Saturation and, Value respectively.
- To close the program, 
  - Close Frame, if in a linux machine.
  - Press q while the Frame window is active, if in a windows machine
  - Interrupt the program by pressing  Ctrl + C in ther terminal and wait for the program to show the Goodbye message
  - If none of the above work, press Ctrl + Z in the terminal and restart the terminal window 


## Troubleshooting

If the file does not run correctly, 
- Reconnect the power to the arm
- Reconnect the arm to the computer
- Reconnect the camera to the computer
- Run IntegratedVisionController.py and reset the home position and move the arm while doing so.

If you have problems with detecting the objects, 
- Reset the thresholds by running
```
python range_detector.py --filter HSV --webcam
```
- make sure the required object is white and there's less 'white' noise :wink:
- Change the HSV sliders one by one, starting from H upper, H lower, going through S and V alternating between upper and lower values 
