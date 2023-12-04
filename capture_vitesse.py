from ivy.std_api import *
import time
import numpy as np

v_lim = [10,10]
v_managed = 10 
v_selected = 10
mode_choisi = "Managed"
val = 0
nx=1
nx_AP_max=1
#nx_max=1 
IAS = 10
fpa = 0
state_vector = {"x":0,"y":0,"z":0,"IAS":0,"fpa":10,"phi":0,"psi":0}

#Partie Ivy
def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent, _id):
    pass

def maj_state_v(agent, *larg):
    IAS = larg[3]
    fpa = larg[4]
    state_vector = {"x":larg[0],"y":larg[1],"z":larg[2],"IAS":larg[3],"fpa":larg[4],"phi":larg[5],"psi":larg[6]}
    return state_vector

def maj_vitesse(agent, *larg):
    v_lim[0],v_lim[1]=larg[0],larg[1]
    return {"vmin":larg[0],"vmax":larg[1]}
    
def maj_vitesse_man(agent, *larg):
    v_managed = larg[0]
    return {"vi":larg[0]}

def mode_choisi(agent, *larg):
    mode_choisi = larg[0]
    val = larg[1]
    if mode_choisi == "SelectedSpeed":
        v_selected = val
    return {"Mode":larg[0], "Val":larg[1]}

def maj_nx(agent, *larg):
    #nx_max = larg[0]
    nx_AP_max = larg[1]
    return {"nx":larg[0], "nx_AP":larg[1]}





#Partie Capture de vitesse

#Si mode sélecté
def vitesse_selected_checked(agent, *larg):
    if v_selected < v_lim[0]:
        v_selected = v_lim[0]

    elif v_selected > v_lim[1] :
        v_selected = v_lim[1]

    else:
        pass    
    return v_selected
    


def capture_vitesse(agent, *larg):
    k11 = 0.08
    if mode_choisi == "Managed":
        nx = (v_managed - IAS)*k11 + np.sin(fpa)
    else:
        nx = (v_selected - IAS)*k11 + np.sin(fpa)

    return nx

def nx_checked(agent, *larg):
    if nx > nx_AP_max:
        nx = nx_AP_max
    else : 
        pass
    return nx


app_name = "FGS_Test"
ivy_bus = "127.255.255.255:2017"
IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(maj_state_v, "^StateVector x=(\S+) y=(\S+) z=(\S+) IAS=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")
IvyBindMsg(maj_vitesse, "^SpeedLimits vmin=(\S+) vmax=(\S+)")
IvyBindMsg(mode_choisi, "^FCUSpeedMach Mode=(\S+) Val=(\S+)") # Mode = Managed, SelectedSpeed
IvyBindMsg(maj_vitesse_man, "^ManagedSpeed vi=(\S+) ")
IvyBindMsg(maj_nx, "^LimitsN nx=(\S+) nz=(\S+) nx_AP=(\S+) nz_AP=(\S+)")
