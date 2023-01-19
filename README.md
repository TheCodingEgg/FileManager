# FileManager
File Manager

A minimal file manager app with graphical interface. It is written in Python
using PySimpleGUI (a minigame written in pygame is embedded as a fun side-activity).
It can be run either

***NATIVELY***
- install Python with Tkinter (under Ubuntu, ```sudo apt install python3 python3-tk```)
- clone our repo ```git clone https://github.com/AlexandruPites/FileManager.git```
- run ```pip install -r requirements.txt```
- in the repo root run ```python3 main.py``` (under Linux) or ```py main.py``` (under Windows)

***CONTAINERISED***
- install docker
- ```docker build -f <path_to_dockerfile> -t filemanager .```
- ```docker run --name ubvnc -p 25901:5901 -p 26901:6901 filemanager```

- go to http://localhost:26901/vnc_lite.html (password is headless)

Contributions from each member:

Alex and Andrei worked on GUI and filetree logic. Alex did the initial architecture and Andrei did the overhaul on some aspects.
Luca did some testing and dockerized the app, wrote the README and handled dependency management.
Difficulties encountered: poor typing of the pyton language and comparatively slow speed compared to a compiled language. The layouts in PySimpleGUI were a headache. Exception handling sometimes makes the application crash. It was a big difficulty to containerize a GUI app in docker.
