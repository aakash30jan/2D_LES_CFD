import numpy as np,sys,time,os,shutil
import numba 
from numba import jit 
import inspect
import json
from functions import *
from ruamel.yaml import YAML
#blah blah blah
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False
# Hello its Me!
# Hello this is papa and mama
def initialize(config_file):
    
    try:
        print('Removing 0 time')
        files=os.listdir()
        for i in files:
            if isfloat(i):
                shutil.rmtree(i)
        
        shutil.rmtree('Constant')
        print('Removed Constant')
        
        shutil.rmtree('Results')
        print('Removed Results')
        
    except:
        print('Results/Constants/0 does not exist')
    try:
        os.makedirs('Constant/')
        print('Created Constants')
        
        os.makedirs('0/')
        print('Created 0')
        
    except:
        print('Running Code with existing Constants/0')

    yaml = YAML()
    with open(config_file) as file: 
        v = yaml.load(file)  
        constant_dict=v['constants']    
        Cons=constant_dict["Cons"]
        rho=constant_dict["rho"]
        N=constant_dict["N"]
        M=constant_dict["M"]
        xmax=constant_dict["xmax"]
        ymax=constant_dict["ymax"]
        atm=constant_dict["atm"]
        T_ref=constant_dict["T_ref"]
        dyf=constant_dict["dyf"]

    nx=N+1
    ny=M+1

    x=np.linspace(0,xmax,nx)
    y=np.linspace(0,ymax,ny)

    X,Y=np.meshgrid(x,y)
    t1=time.time()

    # Points=np.zeros([2,nx,ny])
    # for j in range(ny):
    #     for i in range(nx):
    #         Points[0,i,j]=X[j,i]
    #         Points[1,i,j]=Y[j,i]
    dx,dy=deltas_write_nonuni(nx,ny,xmax,ymax,dyf)
    
    # yep=Grid_plot(dx,dy)
    # print(yep)
    # sys.exit()
    # dx=np.ones([N+1,M+1])*xmax/N
    # dy=np.ones([N+1,M+1])*ymax/M

    Points=np.zeros([2,nx,ny])
    for i in range(1,nx):
        for j in range(ny):
            Points[0,i,j]=Points[0,i-1,j]+dx[i-1,j]
    for i in range(nx):
        for j in range(1,ny):
            Points[1,i,j]=Points[1,i,j-1]+dy[i,j-1]


    write_points(Cons+'Points.txt',Points)

    # Points_read=read_points(Cons+'Points.txt')

    # print(dx)
    # print(dy)
    #print(dx.shape)
    
    write_scalar(Cons+'Dx.txt',dx)
    write_scalar(Cons+'Dy.txt',dy)

    P=np.zeros([nx+1,ny+1])*atm
    write_scalar('0/P.txt',P)

    U_in=np.linspace(0,1,ny+1)
    U=np.zeros([nx+1,ny+1])
    U[0,:]= 1
    # print(U)
    write_scalar('0/U.txt',U)

    V=np.zeros([nx+1,ny+1])
    write_scalar('0/V.txt',V)

    T=np.ones([nx+1,ny+1])*T_ref # Changed

    T[150:152,100:102] = 375

    # print(T)
    write_scalar('0/T.txt',T)

    phi = np.zeros([nx+1,ny+1])

    phi[150:152,100:102] = 40

    write_scalar('0/phi.txt',phi)


    path='0/'
    np.savetxt(path+'P_.txt',P, delimiter='\t',fmt='%.3f')
    np.savetxt(path+'U_.txt',U, delimiter='\t',fmt='%.3f')
    np.savetxt(path+'V_.txt',V, delimiter='\t',fmt='%.3f')
    np.savetxt(path+'T_.txt',T, delimiter='\t',fmt='%.3f')
    np.savetxt(path+'phi_.txt',phi, delimiter='\t',fmt='%.3f')



# initialize()





