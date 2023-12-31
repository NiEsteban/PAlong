from ivy.std_api import *
import time
import numpy as np

# variables globales
v_lim = [10,10]
v_managed = 10 
v_selected = 10
mode_choisi = "Managed"
val = 0
nx_neg_AP = 0
nx_pos_AP = 0
IAS = 10
fpa = 0
z = 0
state_vector = {"x":0,"y":0,"z":0,"IAS":0,"fpa":10,"phi":0,"psi":0}

#Partie Ivy
def on_cx_proc(agent, connected):
    pass

def on_die_proc(agent, _id):
    pass

def maj_state_v(agent, *larg):
    z = larg[2]
    IAS = larg[3]
    fpa = larg[4]
    state_vector = {"x":larg[0],"y":larg[1],"z":larg[2],"IAS":larg[3],"fpa":larg[4],"phi":larg[5],"psi":larg[6]}
    return state_vector

def maj_vitesse(agent, *larg):
    v_lim[0],v_lim[1]=larg[0],larg[1]
    return {"vmin":larg[0],"vmax":larg[1]}
    
def maj_vitesse_managed(agent, *larg):
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
    nx_neg_AP = larg[0]
    nx_pos_AP = larg[1]
    return {"nx_neg_AP":larg[0], "nx_pos_AP":larg[1]}





#Partie Capture de vitesse

#conversion IAS en CAS
def calculer_vitesse_TAS(IAS,z):
    TAS = IAS + 0.01 * IAS * z/600 #Pour passer directement de l'IAS à la TAS: plus 1% de IAS par tranche de 600ft d'altitude 
    return TAS



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
    if nx > nx_pos_AP:
        nx = nx_pos_AP
    elif nx < nx_neg_AP: 
        nx = nx_neg_AP
    else: 
        pass
    return nx


app_name = "FGS_Test"
ivy_bus = "127.255.255.255:2017"
IvyInit(app_name, "[%s ready]" % app_name, 0, on_cx_proc, on_die_proc)
IvyStart(ivy_bus)
IvyBindMsg(maj_state_v, "^StateVector x=(\S+) y=(\S+) z=(\S+) IAS=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)")
IvyBindMsg(maj_vitesse, "^SpeedLimits vmin=(\S+) vmax=(\S+)")
# dépend du mode choisi, si mode managed choisi, val = 0 donc necessite d'avoir la valeur de la vitesse managée cf ligne 107
IvyBindMsg(mode_choisi, "^FCUSpeedMach Mode=(\S+) Val=(\S+)") # Mode = Managed, SelectedSpeed
IvyBindMsg(maj_vitesse_managed, "^ManagedSpeed vi=(\S+) ")
IvyBindMsg(maj_nx, "^LimitsNAP nx_pos_AP=(\S+) nx_neg_AP=(\S+) nz_pos_AP=(\S+) nz_neg_AP=(\S+)")
