import os
file_dir= os.path.dirname(os.path.realpath(__file__))
os.chdir(file_dir)

import numpy as np
from space_discretization import *
from time_integration import *
from matplotlib import pyplot as plt
from error_calculation import *

print('Finite-Difference Advection Diffusion Solver')

# choose parameters for the initial profile
k = 0.0e-3 # dispersion coefficient [m^2/s]
l = 500.0
xW = -l # x-coordinate west boundary [m]
xE = l # x-coordinate east boundary [m]
C00 = .5e0 # maximum of IC [kg/m3]
a = 100.0 # spreading parameter for IC [m]
sigsq0 = a**2/2
M = C00*(2*np.pi*sigsq0)**.5
U = 1

# PERFORM TEST
nx = 1000 # number of segments
Nx = nx + 1 # number of points
adv_order = 3
X,dx = domain(xW,xE,Nx,'Nx')
Mdiff = diffusion(Nx,k,dx)
Madv = advection(Nx,U,dx,adv_order,'periodic')
Mad = Mdiff + Madv

C0 = gaussian(X,C00,a)
dt = 1


# choose a range of time steps
#T0 = 10
#p = list(range(0,35))
#DT = T0/np.power(2*np.ones(len(p)),p)
#
#EexactHeun = np.zeros(len(DT))
#EnumHeun =  np.zeros(len(DT))

#for i in range(len(DT)):
#    
#    tend = DT[i]
#    
#    Cend = Heun(DT[i],tend,Mad,C0,X) 
#    Can = analytical_sol(sigsq0,M,U,k,X,DT[i])
#    EexactHeun[i] = np.linalg.norm(Can-Cend)*dx**.5
#    enum = num_error(X,sigsq0,M,k,U,dx,DT[i],'Heun')
#    EnumHeun[i] = np.linalg.norm(enum)
    
    
#EexactDIRK2 = np.zeros(len(DT))
#EnumDIRK2 =  np.zeros(len(DT))
#
#for i in range(len(DT)):
#    
#    tend = DT[i]
#    
#    Cend = DIRK2(DT[i],tend,Mad,C0,X) 
#    Can = analytical_sol(sigsq0,M,U,k,X,DT[i])
#    EexactHeun[i] = np.linalg.norm(Can-Cend)*dx**.5
#    enum = num_error(X,sigsq0,M,k,U,dx,DT[i],'DIRK2')
#    EnumHeun[i] = np.linalg.norm(enum)    

def conv_rate(x,DT,expected_cr):
    
    lx0 = np.log(np.abs(x[0]))
    lxEnd = np.log(np.abs(x[-1]))    
    lt0 = np.log(np.abs(DT[0]))
    ltEnd = np.log(np.abs(DT[-1]))    

    lEx = lxEnd - expected_cr*ltEnd
    
    cr = (lxEnd - lx0 )/(ltEnd - lt0)   
    conv_line = np.exp(lEx + expected_cr*np.log(DT))
    
    return cr, conv_line

#cr, cl = conv_rate(EexactHeun,DT,1)

#print(cr)

#diffE = np.abs(EexactHeun-EnumHeun)
#relE = diffE/EexactHeun

fst = 30
fsst = 30
fslb = 30
fsg = 40
lw = 2
ms = 30
mew = 10
wim = 1920
###############################################3
him = wim
my_dpi = 96

#fig1 = plt.figure(figsize=(wim/my_dpi, him/my_dpi), dpi=my_dpi)
#l1, = plt.loglog(DT,EexactHeun,'-Db',markersize=ms,markeredgewidth = mew, linewidth = lw,label='$e_{num} = y_{numerical} - y_{exact}$')
#l2, = plt.loglog(DT,EnumHeun,'--or',markersize=ms,linewidth = lw,label='$e_{analytical}$', markeredgewidth=mew,markeredgecolor='r', markerfacecolor='None')
#l3, = plt.loglog(DT,diffE,'+:g',markersize=ms,markeredgewidth = mew/2,linewidth = lw,label='$=|e_{num} - e_{exact}|$')
#l4, = plt.loglog(DT,relE,':xb',markersize=ms,markeredgewidth = mew/2,linewidth = lw,label='$= \\frac{|e_{num} - e_{analytical}|}{|e_{numerical}|}$')
#plt.legend(handles=[l1,l2,l3,l4],fontsize = fsg,loc='upper center', bbox_to_anchor=(0.5, -0.05))
#plt.title("Heun's method total local truncation error \n PDE: advection-diffusion $t_{end} = dt$",fontsize=fsst)    
#plt.xlabel('dt',fontsize=fslb)
#
#plt.tick_params(axis='both', which='major', labelsize=40)
#fig1.savefig('lte_AD_Heun.png', bbox_inches='tight',dpi=400)

######################
# choose a range of time steps
q = 8
T0 = 2**q
p = list(range(3,13))
DT = T0/np.power(2*np.ones(len(p)),p)

tend = T0
# advected coordinates
Can = analytical_sol(sigsq0,M,U,k,X,tend,l)
check = np.linalg.norm(Can-C0)

#fig0, ax0 = plt.subplots()
#plt.plot(X,C0,'--')
#plt.plot(X,Can,':or')

EexactHeun = np.zeros(len(DT))
for i in range(len(DT)):
    
    Cend = Heun(DT[i],tend,Mad,C0,X) 

    EexactHeun[i] = np.linalg.norm(Can-Cend)*dx**.5

EexactDIRK2 = np.zeros(len(DT))
for i in range(len(DT)):
    
    Cend = DIRK2(DT[i],tend,Mad,C0,X) 

    EexactDIRK2[i] = np.linalg.norm(Can-Cend)*dx**.5
    
EexacttRule = np.zeros(len(DT))
for i in range(len(DT)):
    
    Cend = tRule(DT[i],tend,Mad,C0,X) 

    EexacttRule[i] = np.linalg.norm(Can-Cend)*dx**.5


def conv_rate(x,DT,expected_cr,end_pt = len(DT)):
    
    lx0 = np.log(np.abs(x[0]))
    lxEnd = np.log(np.abs(x[-1]))    
    lt0 = np.log(np.abs(DT[0]))
    ltEnd = np.log(np.abs(DT[-1]))    

    lEx = np.log(np.abs(x[end_pt-1])) - expected_cr*np.log(np.abs(DT[end_pt-1])) 
    
    cr = (lxEnd - lx0 )/(ltEnd - lt0)   
    conv_line = np.exp(lEx + expected_cr*np.log(DT))
    
    return cr, conv_line

cr, cl = conv_rate(EexacttRule,DT,2,3)
plt.close("all")
him = wim
my_dpi = 96
fig2 = plt.figure(figsize=(wim/my_dpi, him/my_dpi), dpi=my_dpi)
sp0 = 6
sp1 = 0
ep=-4

l2, = plt.loglog(DT[sp1:],EexactDIRK2[sp1:],':+',markersize=ms,markeredgewidth = mew, linewidth = lw,label='DIRK2')
l3, = plt.loglog(DT[sp1:],EexacttRule[sp1:],':x',markersize=ms,markeredgewidth = mew, linewidth = lw,label='trap rule')
l4, = plt.loglog(DT[0:ep],cl[0:ep],'--k',label='2nd order')
l1, = plt.loglog(DT[sp0:],EexactHeun[sp0:],':o',markersize=ms,linewidth = lw,label='Heun', markeredgewidth=mew,markeredgecolor='r', markerfacecolor='None')
plt.title("time converge \n 2nd order upwind space discretization",fontsize=fsst)    

plt.legend(handles=[l1,l2,l3,l4],fontsize = fsg)
plt.tick_params(axis='both', which='major', labelsize=40)
fig2.savefig('conv_plots.png', bbox_inches='tight',dpi=400)