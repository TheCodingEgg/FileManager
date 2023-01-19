# FileManager
File Manager

A minimal file manager app with graphical interface. It is written in Python
using PySimpleGUI (a minigame written in pygame is embedded as a fun side-activity).
It can be run either

***NATIVELY***
- install Python with Tkinter (under Ubuntu, ```sudo apt install python3 python3-tkinter```)
- clone our repo ```git clone https://github.com/AlexandruPites/FileManager.git```
- run ```pip install requirements.txt```
- in the repo root run ```python3 main.py``` (under Linux) or ```py main.py``` (under Windows)

***CONTAINERISED***
- install docker
- ```docker pull accetto/ubuntu-vnc-xfce-python-g3
docker build -f <path_to_dockerfile> -t filemanager .
docker run --name ubvnc -p 25901:5901 -p 26901:6901 filemanager```

- go to http://localhost:26901/vnc_lite.html (password is headless)

Contribuțiile fiecărui membru:
- Alex și Andrei au lucrat pe GUI și logica filetreeului. Alex a făcut arhitectura
inițială și Andrei a făcut overhaul pe anumitea aspecte.
- Luca a făcut ceva testing și a dockerizat appul, a scris READMEul și s-a ocupat
de dependency management.

Dificultăți întâmpinate: tiparea slabă a limbajului pyton și viteza comparativ
înceată cu a unui limbaj compilat. Layouturile din PySimpleGUI au dat bătăi de cap.
A constituit o dificultate mare să containerizez un app cu GUI în docker. 
