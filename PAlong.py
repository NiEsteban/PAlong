from ivy.std_api import *
import time
import numpy as np 
import matplotlib.pyplot as plt
alt_mode = "Managed" #Selected ou FPA ou VS
v_mode = "Managed" 
alt_c=float
v_c_TAS=float
fpa_vz_c=float



k11 = 0.08
k22 = 2
nx_min = float
nx_max = float
nz_min = float
nz_max = float
nz= float
nx=float
V_lim=[float,float]

state_vector = {"x":float,"y":float,"z":float,"TAS":float,"fpa":float,"phi":float,"psi":float}
def op(agent, connected):
    pass


def cl(agent,_id):
    IvyStop()
def set_limits(agent,*larg):
    global nx_min = larg[0]
    global nx_max = larg[0]
    global nz_min = larg[0]
    global nz_max = larg[0]

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
    global state_vector = {"x":larg[0],"y":larg[1],"z":larg[2],"TAS":calculer_vitesse_TAS(larg[3],larg[2]),"fpa":larg[4],"phi":larg[5],"psi":larg[6]}
    return state_vector

def maj_vitesse(agent, *larg):
    global v_lim[0],v_lim[1]=larg[0],larg[1]
    return V_lim



def capture_pente(agent, *larg):
    eplison = 1 #tolérance en m/s  
    while calculer(abs(v_c-state_vector["TAS"])>epsilon):
        pass
    global alt_c = larg[0]
    global alt_mode = larg[1]
    global fpa_vz_c = larg[2]
    if alt_mode == "Selected":
        global nz = ((alt_c-z)/v*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
    elif alt_mode == 'FPA':
        global nz = (((fpa_vz_c - state_vector("fpa"))*k22) + np.cos(state_vector("fpa")))/np.cos("phi")
    elif alt_mode == 'VS':
        global nz = (((np.arcsin(fpa_vz_c/TAS) - state_vector("fpa"))*k22) + np.cos(state_vector("fpa")))/np.cos("phi")
    else:
         print("Error capt pente")

         
def capture_pente_managed(agent, *larg):
    eplison = 1 #tolérance en m/s  
    while calculer(abs(v_c-state_vector["TAS"])>epsilon):
        pass
    if alt_mode == "Managed":
        global nz = ((zc-z)/v*k11-state_vector["fpa"])*k22+np.cos(state_vector["fpa"])/np.cos(state_vector["phi"])
    else:
        print("Error capt pente managed")
    return apply_lim(nz,nz_min,nz_max)

def capture_vitesse(agent, *larg):
    global v_mode =larg[0]
    global v_c_TAS=calculer_vitesse_TAS(larg[1],state_vector["z"])
    eplison = 2 #tolérance en m  
    while calculer(abs(alt_c-state_vector["z"])>epsilon):
        pass
    if v_mode == "Selected":
        global nx = (apply_lim(v_c_TAS,v_lim[0],v_lim[1]) - state_vector["TAS"])*k11 + np.sin(state_vector["fpa"])
        return apply_lim(nx,nx_min,nx_max)
    else: 
        print("Error capt vitesse") #on attend de recevoir le message du fgs avec la vitesse managed

def capture_vitesse_managed(agent, *larg):
    global v_managed = calculer_vitesse_TAS(larg[0],state_vector["z"])
    global nx = (v_managed - state_vector["TAS"])*k11 + np.sin(state_vector["fpa"])
    eplison = 2 #tolérance en m  
    while calculer(abs(alt_c-state_vector["z"])>epsilon):
        pass
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

