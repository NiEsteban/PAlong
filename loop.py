from ivy.std_api import *
import time
import numpy as np 
import matplotlib.pyplot as plt
speed_mode = 0 #selected : 0, managed = 1
alt_mode = "Managed" #Selected ou FPA ou VS
nz=1
nx=1
lim_nx=
lim_nz=
state_vector = {"x":0,"y":0,"z":0,"IAS":0,"fpa":0,"phi":0,"psi":0}
def op(agent, connected):
    pass


def cl(agent,_id):
    IvyStop()



def msg(agent, *larg):
    print(larg)

def maj_state_v(agent, *larg):
    state_vector = {"x":larg[0],"y":larg[1],"z":larg[2],"IAS":larg[3],"fpa":larg[4],"phi":larg[5],"psi":larg[6]}
    return state_vector
def capture_pente(agent, *larg):


    return (nz,nx)

def capture_alt(agent, *larg):
    alt_mode = larg[2]
    zc = larg[1]
    if alt_mode == 0 :
        t = np.linspace(0,500,501)
        dt=1/500
        state_vector["fpa"] = np.arcsin(zc-state_vector["z"]/state_vector["IAS"]*dt)


        return (nz,nx)
    else:




        return (nz,nx)


app_n ="Testap"
ivy_bus ="10.3.49.7"
IvyInit(app_n ,"ready" ,0 ,op ,cl )
IvyStart(ivy_bus)
time.sleep(10)
IvyBindMsg(maj_state_v,'^mot1=(\S+)')
IvyBindMsg(capture_alt,'^ManagedAlt alt=(\S+) Q=(\S+)')
IvyBindMsg(capture_alt,'^FCUVertical Altitude=(\S+) Mode=(\S+) Val=(\S+)')
IvyBindMsg(capture_vitesse,'^FCUSpeedMach Mode=(\S+) Val=(\S+)')
IvyMainLoop()


