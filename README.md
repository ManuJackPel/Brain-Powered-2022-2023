# Brain-Powered-2022-2023
The repository of a UvA honours course: Brain Powered 2022/2023, which is a project with the goal of designing and writing an algorithm that allows one to control a drone with their mind. Using EEG we want to measure signals coming from the motor cortex and extract the unqiue features from these signals that correlate with motor activity responsible for movement in the left and right hands and feet.

# EEG data acquisition and streaming to python environment:
OpenVibe EEG stream.xml: replacement for matlab. The OpenVibe software (version 1.2.1) includes a driver for the g.Mobilab. The script opens an LSL server to which it streams the raw EEG data.

lslstream.py: Parses the raw, live EEG data from the LSL server streamed by OpenVibe.

LSL: Lab Streaming Layer, a communication protocol designed to stream between a server and a multitude of programming environments. Designed for use in scientific data acquisition.

OpenVibe: software designed to easily create BCI programs. Includes drivers, multiple data transformation methods and LSL streaming capabilities.

Drivers and software:

PL2303_Prolific_DriverInstaller_v1_12_0
Driver for the VGA to USB adapter on the g.Mobilab
https://www.lmt.de/latest/Drivers/USB,%20PCIe-serial/PL2303_Prolific_DriverInstaller_v1_12_0/

OpenVibe + g.Mobilab driver:
http://openvibe.inria.fr/forum/viewtopic.php?p=13859
http://openvibe.inria.fr/pub/bin/win32/
 (openvibe-gmobilab-1.2.1-setup.exe, of .. wij gebruiken nu openvibe-gmobilab-1.1.0-setup.exe)

Standalone OpenVibe scenario player to run the scripts (scenarios) without using the OpenVibe designer GUI
http://openvibe.inria.fr/standalone-scenario-player/

Python script to download the EEG data from the LSL server
https://github.com/labstreaminglayer/liblsl-Python/blob/master/pylsl/examples/ReceiveData.py

PyLSL library which allows this:
pip install pylsl
