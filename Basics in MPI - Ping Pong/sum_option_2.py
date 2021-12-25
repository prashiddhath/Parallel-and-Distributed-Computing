#!/usr/bin/env python
from mpi4py import MPI
import sys

world_size = MPI.COMM_WORLD.Get_size()
world_rank = MPI.COMM_WORLD.Get_rank()

comm = MPI.COMM_WORLD

local_value = world_rank


if world_rank!=0:
    current_sum = comm.recv(source=world_rank-1, tag=0)
else:
    current_sum = 0
    
current_sum = current_sum+local_value

if world_rank<world_size-1:
    comm.send(current_sum,dest=world_rank+1,tag=0)

if world_rank==world_size-1:
    for r in range(world_size):
        comm.send(current_sum, dest=r, tag=0)

sum = comm.recv(source=world_size-1,tag=0)

print("The sum is %d" % sum)


