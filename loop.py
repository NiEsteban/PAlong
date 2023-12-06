from ivy.std_api import *
import time
import numpy as np 
import matplotlib.pyplot as plt
alt_mode = "Managed" #Selected ou FPA ou VS
V_mode = "Managed" 
k11 = 0.08
k22 = 2
nx_min = 0
nx_max = 1
nz_min = 0
nz_max = 1
nz=1
nx=1
V_lim=[0,0]

state_vector = {"x":0,"y":0,"z":0,"TAS":0,"fpa":0,"phi":0,"psi":0}
def op(agent, connected):
    pass


def cl(agent,_id):
    IvyStop()
def set_limits(agent,*larg):
    nx_min = larg[0]
    nx_max = larg[0]
    nz_min = larg[0]
    nz_max = larg[0]
    return 0

def apply_lim(value, min, max):
    if value>max:
        return max
    elif value < min:
        return min
    else value

def msg(agent, *larg):
    print(larg)

def calculer_vitesse_TAS(IAS,z):
    TAS = IAS + 0.01 * IAS * z/600 #Pour passer directement de l'IAS à la TAS: plus 1% de IAS par tranche de 600ft d'altitude 
    return TAS

def maj_state_v(agent, *larg):
    state_vector = {"x":larg[0],"y":larg[1],"z":larg[2],"TAS":calculer_vitesse_TAS(larg[3],larg[2]),"fpa":larg[4],"phi":larg[5],"psi":larg[6]}
    return state_vector

def maj_vitesse(agent, *larg):
    v_lim[0],v_lim[1]=larg[0],larg[1]
    return V_lim



def capture_pente(agent, *larg):
    alt_cons = larg[0]
    alt_mode = larg[1]
    value = larg[2]
    if alt_mode == "Selected":
        nz = ((alt_cons-z)/v*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
    elif alt_mode == 'FPA':
        nz = (((value - state_vector("fpa"))*k22) + np.cos(state_vector("fpa")))/np.cos("phi")
    elif alt_mode == 'VS':
        nz = (((np.arcsin(value/TAS) - state_vector("fpa"))*k22) + np.cos(state_vector("fpa")))/np.cos("phi")



def capture_pente_managed(agent, *larg):
    if alt_mode == "Managed":
        nz = ((zc-z)/v*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
    else:
    return apply_lim(nz,nz_min,nz_max)


def capture_vitesse(agent, *larg):
    v_mode =larg[0]
    if v_mode == "Selected":
        nx = (apply_lim(v_selected,v_lim[0],v_lim[1]) - state_vector["TAS"])*k11 + np.sin(state_vector["fpa"])
        return apply_lim(nx,nx_min,nx_max)
    else: 
        pass #on attend de recevoir le message du fgs avec la vitesse managed


def capture_vitesse_managed(agent, *larg):
    v_managed = calculer_vitesse_TAS(larg[0],state_vector["z"])
    nx = (v_managed - state_vector["TAS"])*k11 + np.sin(state_vector["fpa"])
    return apply_lim(nx,nx_min,nx_max)#pas nécessaire apply_lim car déjà verifier par le fgs

app_n ="PAlong"
ivy_bus ="10.3.49.7"
IvyInit(app_n ,"ready" ,0 ,op ,cl )
IvyStart(ivy_bus)
time.sleep(1)
IvyBindMsg(set_limits,'^LimitsN nx_neg=(\S+) nx_pos=(\S+) nz_neg=(\S+) nz_pos=(\S+)')
IvyBindMsg(capture_pente_managed,'^ManagedAlt alt=(\S+) Q=(\S+)')
IvyBindMsg(capture_pente,'^FCUVertical Altitude=(\S+) Mode=(\S+) Val=(\S+)')
IvyBindMsg(capture_vitesse,'^FCUSpeedMach Mode=(\S+) Val=(\S+)')
IvyBindMsg(capture_vitesse_managed, "^ManagedSpeed vi=(\S+)")
IvyMainLoop()

