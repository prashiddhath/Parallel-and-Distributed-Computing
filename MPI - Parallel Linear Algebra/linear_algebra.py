#!/usr/bin/env python
from mpi4py import MPI

import iohelper as io

def add_vecs(x, y, M, comm):
    local_M = int(M / comm.Get_size())

    z = x
    for i in range(local_M):
        z[i] = z[i] + y[i]
        
    return z


def dot_product(x,y, M, comm):
    local_M = int(M / comm.Get_size())
    
    local_sum = 0
    for i in range(local_M):
        local_sum = local_sum + x[i]*y[i]

    sum = comm.allreduce(local_sum) 
    return sum


def mat_vec_mult(A,x, M, N, comm):
    local_M = int(M / comm.Get_size())

    global_x = comm.allgather(x)
    global_x = [item for sublist in global_x for item in sublist]
    
    y = [0]*local_M
    for i in range(local_M):
        y[i] = 0
        for j in range(N):
            y[i] = y[i] + A[i*N+j]*global_x[j]
    return y


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

y1,M = io.read_vec_from_file('y1.csv',comm)
y2,M = io.read_vec_from_file('y2.csv',comm)
x,N = io.read_vec_from_file('x.csv',comm)
A,M,N = io.read_mat_from_file('A.csv',comm)

io.print_vec(x, N, comm)
io.print_vec(y1, M, comm)
io.print_mat(A, M, N, comm)

y3 = add_vecs(y1, y2, M, comm)
io.print_vec(y3,M,comm)

prod = dot_product(y1, y2, M, comm)
print(prod)

y = mat_vec_mult(A, x, M, N, comm)
io.print_vec(y,M,comm)

