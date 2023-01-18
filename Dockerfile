FROM accetto/ubuntu-vnc-xfce-python-g3

ADD main.py .
USER root
RUN adduser --disabled-password --gecos '' docker
RUN adduser docker sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker

RUN sudo apt update
RUN sudo apt install python3-tk -y

USER root
RUN pip install PySimpleGUI

CMD ["python3", "./main.py"]
