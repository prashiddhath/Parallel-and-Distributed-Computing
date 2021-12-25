FROM deepnote/python:3.7

RUN sudo apt-get update -y
RUN sudo apt-get install -y openmpi-bin libopenmpi-dev build-essential
RUN echo "localhost slots=8" >> /etc/openmpi/openmpi-default-hostfile
RUN pip install mpi4py
RUN adduser --disabled-password --shell /bin/bash --gecos "User" --uid 1000 user