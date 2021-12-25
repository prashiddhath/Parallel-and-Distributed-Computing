#!/usr/bin/env python
from mpi4py import MPI
import sys

world_size = MPI.COMM_WORLD.Get_size()
world_rank = MPI.COMM_WORLD.Get_rank()

comm = MPI.COMM_WORLD

local_value = world_rank

comm.send(local_value, dest=0, tag=0)

sum = 0
if world_rank==0:
    for r in range(world_size):
        received_value = comm.recv(source=r, tag=0)
        sum = sum + received_value

    for r in range(world_size):
        comm.send(sum, dest=r, tag=0)


sum = comm.recv(source=0, tag=0)
print("The sum is %d." % sum)

