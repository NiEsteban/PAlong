from ivy.std_api import *
import time
import numpy as np 
import matplotlib.pyplot as plt
speed_mode = 0 #selected : 0, managed = 1
alt_mode = "Managed" #Selected ou FPA ou VS
k11 = 0.08
k22 = 2
nz_max = 10
nz_min = 0
nz=1
nx=1
lim_nx=0
lim_nz=0
odl_state = {"x":0,"y":0,"z":0,"IAS":0,"fpa":0,"phi":0,"psi":0}
state_vector = {"x":0,"y":0,"z":0,"IAS":0,"fpa":0,"phi":0,"psi":0}
def op(agent, connected):
    pass


def cl(agent,_id):
    IvyStop()

def apply_lim(value, max, min=0):
    if value>max:
        return max
    elif value < min:
        return min
    else value

def msg(agent, *larg):
    print(larg)

def maj_state_v(agent, *larg):
    state_vector = {"x":larg[0],"y":larg[1],"z":larg[2],"IAS":larg[3],"fpa":larg[4],"phi":larg[5],"psi":larg[6]}
    return state_vector
def capture_pente(agent, *larg):


    return (nz,nx)

def capture_alt(agent, *larg):
    alt_mode = larg[2]
    if alt_mode == "Selected":
        zc = larg[1]
        nz = ((zc-z)/v*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
        return apply_lim(nz,nz_max,nz_min)
    elif alt_mode == "Managed":
        nz = ((zc-z)/v*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
        return apply_lim(nz,nz_max,nz_min)
    elif alt_mode == "FPA":




        return apply_lim(nz,nz_max,nz_min)


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


