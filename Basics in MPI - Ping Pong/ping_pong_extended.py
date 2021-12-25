#!/usr/bin/env python
from mpi4py import MPI
import sys

world_size = MPI.COMM_WORLD.Get_size()
world_rank = MPI.COMM_WORLD.Get_rank()

comm = MPI.COMM_WORLD

if world_rank==0:
    initial_value_to_be_sent = 41
    dest = 1
    source = dest
    received_value=0

    value_to_be_sent = initial_value_to_be_sent

    for i in range(4):
        comm.send(value_to_be_sent, dest=dest, tag=0)
        received_value = comm.recv(source=source, tag=0)
        print("The received answer is %d" % received_value)
        value_to_be_sent = received_value



elif world_rank==1:
    received_value = 0
    source = 0
    dest = source
    
    for i in range(4):
        received_value = comm.recv(source=source, tag=0)
        new_value = received_value+1
        comm.send(new_value, dest=dest, tag=0)
