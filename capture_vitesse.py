from ivy.std_api import *
import time
import numpy as np

g = 9.81
v_lim = [10,10]
v_managed = 10
mode_choisi = "X"
val = 0

def on_cx_proc(agent, connected):
    pass

def on_msg1(agent, *larg):
    print("Reception: Vp={}, fpa={}".format(larg[3], larg[4]))

def on_msg2(agent, *larg):
    print("Reception: selected={}, capture={}".format(larg[0], larg[1]))

def on_die_proc(agent, _id):
    pass

def maj_state_v(agent, *larg):
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
    return {"Mode":larg[0], "Val"=larg[1]}


#Si mode sélecté
def vitesse_selected(agent, *larg):
    if V_selected < v_lim[0]:
        V_selected = v_lim[0]
    elif V_selected > v_lim[1] :
        V_selected = v_lim[1]
    else:
        pass    
    return V_selected
    
#Si mode managé


def capture_vitesse(agent, *larg):
    k11 = 0.08
    nx = (V_selected - larg[3])*k11 + np.sin(larg[4]) #v_dot = vitesse_selected(agent, *larg).dot

    return nx


app_name = "FGS_Test"
ivy_bus = "127.255.255.255:2017"
IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(maj_state_v, "^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")
IvyBindMsg(maj_vitesse, "^SpeedLimits vmin=(\S+) vmax=(\S+)")
IvyBindMsg(mode_choisi, "^FCUSpeedMach Mode=(\S+) Val=(\S+)") # Mode = Managed, SelectedSpeed
IvyBindMsg(maj_vitesse_man, "^ManagedSpeed vi=(\S+) ")