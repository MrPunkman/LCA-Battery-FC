from timeit import default_timer as timer
from openlca_automation.tool import lca
#import gradio as gr
import olca
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from vehicleDef import *
from oLCAInventory import *
from energyMixDef import *
import textwrap


savepath = r'C:\Users\Leonard\tubCloud2\00_Uni\01_Paper-Projekt-LCA-PEMFC\04-Plots\Trucks\\'
# vehicle standards, lifetime in years, kmPerYear in km
lifetime = 12
kmPerYear40t = 67415
kmPerYear25t = 95000
kmPerYear18t = 115000

# set e-mix
## Germany
electricity2021Gemany = 0.475                       # kg CO2 /kWh
electricity2050Germany = 0.175                       # kg CO2 /kWh

## EU
electricity2021EU = 0.427                       # kg CO2 /kWh
electricity2050EU = 0.12100                       # kg CO2 /kWh

electricityInterpolation = np.linspace(electricity2021EU,electricity2050EU,50-21)


h2Prod2021 = 15.37125                           # kg CO2 / kWh
h2Prod2050 = 6.45773                           # kg CO2 / kWh
h2Interpolation = np.linspace(h2Prod2021,h2Prod2050,50-21)

# meinEnergieMixEAuto = EnergyMix(nuclear=3.98, geothermal=0.03,rbiomass=7.72, coal=15.25,wind=39.35,solar=25.39,water=1.9,pump=9.05,gas=5.09,oil=0.01)
# meinEnergieMixFCAuto = EnergyMix(nuclear=3.98, geothermal=0.03,rbiomass=7.72, coal=15.25,wind=39.35,solar=25.39,water=1.9,pump=9.05,gas=5.09,oil=0.01)

### for 40 t:

Truck40FCNMC811_300_100 = Truck(name = "40 t FC 300 B 100",payloadfactor=1, gvW = 40, laufLeistungProJahr=kmPerYear40t,cellchem='NMC811', lebensDauer=12, batteryCap= 100, consumption = 9.7, fcLeistung = 300, h2Cap=25)
Truck40FCNMC811_150_72 = Truck(name = "40 t FC 150 B 72",payloadfactor=1, gvW = 40, laufLeistungProJahr=kmPerYear40t,cellchem='NMC811', lebensDauer=12, batteryCap= 72, consumption = 9.25, fcLeistung = 150, h2Cap=25)
# Truck40FCNMC111_300_100 = Truck(name = "Truck40FCNMC111 FC 300 B 100 40 t",gvW = 40, laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 100, consumption = 9.7, fcLeistung = 300, h2Cap=25)
# Truck40FCNCA_300_100 = Truck(name = "Truck40FCNCA FC 300 B 100 40 t",gvW = 40, laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 100, consumption = 9.7, fcLeistung = 300, h2Cap=25)
# Truck40FCLFP_300_100 = Truck(name = "Truck40FCLFP FC 300 B 100 40 t",gvW = 40, laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 100, consumption = 9.7, fcLeistung = 300, h2Cap=25)

Truck40NMC811_EFORCE = Truck(name = "40 t EFORCE",payloadfactor=1, gvW = 40,laufLeistungProJahr=kmPerYear40t,cellchem='NMC811', lebensDauer=12, batteryCap= 450, vehrange=260)
# Truck40NMC111_EFORCE = Truck(name = "Truck40NMC111 EFORCE 40 t",gvW = 40,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 450, vehrange=260)
# Truck40NCA_EFORCE = Truck(name = "Truck40NCA EFORCE 40 t",gvW = 40,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 450, vehrange=260)
# Truck40LFP_EFORCE = Truck(name = "Truck40LFP EFORCE 40 t",gvW = 40,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 450, vehrange=260)


Truck40FCNMC811_Daimler = Truck(name = "40 t Daimler",payloadfactor=0.5, gvW = 40,laufLeistungProJahr=kmPerYear40t,cellchem='NMC811', lebensDauer=12, batteryCap= 336, vehrange=220)
# Truck40NMC111_Daimler = Truck(name = "Truck40NMC111 Daimler 40 t",gvW = 40,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 336, vehrange=220)
# Truck40NCA_Daimler = Truck(name = "Truck40NCA Daimler 40 t",gvW = 40,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 336, vehrange=220)
# Truck40LFP_Daimler = Truck(name = "Truck40LFP Daimler 40 t",gvW = 40,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 336, vehrange=220)





### for 25 t:

Truck25FCNMC811_300_100 = Truck(name = "25 t FC 300 B 100", gvW = 25, payloadfactor=1, laufLeistungProJahr=kmPerYear25t,cellchem='NMC811', lebensDauer=12, batteryCap= 100, consumption = 7.21, fcLeistung = 300, h2Cap=25)
Truck25FCNMC811_150_72 = Truck(name = "25 t FC 150 B 72", gvW = 25, payloadfactor=1, laufLeistungProJahr=kmPerYear25t,cellchem='NMC811', lebensDauer=12, batteryCap= 72, consumption = 6.81, fcLeistung = 150, h2Cap=25)
# Truck40FCNMC111_300_100 = Truck(name = "Truck40FCNMC111 FC 300 B 100 25 t",gvW = 25, laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 100, consumption = 7.21, fcLeistung = 300, h2Cap=25)
# Truck40FCNCA_300_100 = Truck(name = "Truck40FCNCA FC 300 B 100 25 t",gvW = 25, laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 100, consumption = 7.21, fcLeistung = 300, h2Cap=25)
# Truck40FCLFP_300_100 = Truck(name = "Truck40FCLFP FC 300 B 100 25 t",gvW = 25, laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 100, consumption = 7.21, fcLeistung = 300, h2Cap=25)

Truck25NMC811_EFORCE = Truck(name = "25 t EFORCE", gvW = 25, payloadfactor=1,laufLeistungProJahr=kmPerYear25t,cellchem='NMC811', lebensDauer=12, batteryCap= 450, vehrange=300)
# Truck40NMC111_EFORCE = Truck(name = "Truck40NMC111 EFORCE 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 450, vehrange=300)
# Truck40NCA_EFORCE = Truck(name = "Truck40NCA EFORCE 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 450, vehrange=300)
# Truck40LFP_EFORCE = Truck(name = "Truck40LFP EFORCE 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 450, vehrange=300)


Truck25FCNMC811_Daimler = Truck(name = "25 t Daimler", payloadfactor=0.5, gvW = 25,laufLeistungProJahr=kmPerYear25t,cellchem='NMC811', lebensDauer=12, batteryCap= 336, vehrange=300)
# Truck40NMC111_Daimler = Truck(name = "Truck40NMC111 Daimler 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 336, vehrange=300)
# Truck40NCA_Daimler = Truck(name = "Truck40NCA Daimler 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 336, vehrange=300)
# Truck40LFP_Daimler = Truck(name = "Truck40LFP Daimler 25 t",gvW =25,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 336, vehrange=300)

Truck25FCNMC811_Daimler_re = Truck(name = "25 t Daimler ER", payloadfactor=0.5, gvW = 25,laufLeistungProJahr=kmPerYear25t,cellchem='NMC811', lebensDauer=12, batteryCap= 448, vehrange=400)

# Truck40NMC111_Daimler_re = Truck(name = "Truck40NMC111 Daimler ER 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 448, vehrange=400)
# Truck40NCA_Daimler_re = Truck(name = "Truck40NCA Daimler ER 25 t",gvW = 25,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 448, vehrange=400)
# Truck40LFP_Daimler_re = Truck(name = "Truck40LFP Daimler ER 25 t",gvW =25,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 448, vehrange=400)


### for 18 t:
Truck18FCNMC811_300_100 = Truck(name = "18 t FC 300 B 100", payloadfactor=1, gvW = 18, laufLeistungProJahr=kmPerYear18t,cellchem='NMC811', lebensDauer=12, batteryCap= 100, consumption = 6.81, fcLeistung = 300, h2Cap=25)
Truck18FCNMC811_150_72 = Truck(name = "18 t FC 150 B 72", payloadfactor=1, gvW = 18, laufLeistungProJahr=kmPerYear18t,cellchem='NMC811', lebensDauer=12, batteryCap= 72, consumption = 6.56, fcLeistung = 150, h2Cap=25)
# Truck40FCNMC111_300_100 = Truck(name = "Truck40FCNMC111 FC 300 B 100 18 t",gvW = 18, laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 100, consumption = 6.81, fcLeistung = 300, h2Cap=25)
# Truck40FCNCA_300_100 = Truck(name = "Truck40FCNCA FC 300 B 100 18 t",gvW = 18, laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 100, consumption = 6.81, fcLeistung = 300, h2Cap=25)
# Truck40FCLFP_300_100 = Truck(name = "Truck40FCLFP FC 300 B 100 18 t",gvW = 18, laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 100, consumption = 6.81, fcLeistung = 300, h2Cap=25)

Truck18NMC811_EFORCE = Truck(name = "18 t EFORCE", payloadfactor=1, gvW = 18,laufLeistungProJahr=kmPerYear18t,cellchem='NMC811', lebensDauer=12, batteryCap= 450, vehrange = 350)
# Truck40NMC111_EFORCE = Truck(name = "Truck40NMC111 EFORCE 18 t",gvW = 18,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 450, vehrange=350)
# Truck40NCA_EFORCE = Truck(name = "Truck40NCA EFORCE 18 t",gvW = 18,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 450, vehrange=350)
# Truck40LFP_EFORCE = Truck(name = "Truck40LFP EFORCE 18 t",gvW = 18,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 450, vehrange=350)


Truck18FCNMC811_Daimler = Truck(name = "18 t Daimler", payloadfactor=0.5, gvW = 18,laufLeistungProJahr=kmPerYear18t,cellchem='NMC811', lebensDauer=12, batteryCap= 336, vehrange = 330)
# Truck40NMC111_Daimler = Truck(name = "Truck40NMC111 Daimler 18 t",gvW = 18,laufLeistungProJahr=67416.6,cellchem='NMC111', lebensDauer=12, batteryCap= 336, vehrange=330)
# Truck40NCA_Daimler = Truck(name = "Truck40NCA Daimler 18 t",gvW = 18,laufLeistungProJahr=67416.6,cellchem='NCA', lebensDauer=12, batteryCap= 336, vehrange=330)
# Truck40LFP_Daimler = Truck(name = "Truck40LFP Daimler 18 t",gvW = 18,laufLeistungProJahr=67416.6,cellchem='LFP', lebensDauer=12, batteryCap= 336, vehrange=330)



vehicles = [Truck40FCNMC811_300_100,Truck40FCNMC811_150_72,Truck40NMC811_EFORCE,Truck40FCNMC811_Daimler,                               # 40 t
            Truck25FCNMC811_300_100,Truck25FCNMC811_150_72,Truck25NMC811_EFORCE,Truck25FCNMC811_Daimler,Truck25FCNMC811_Daimler_re,    # 25 t
            Truck18FCNMC811_300_100,Truck18FCNMC811_150_72,Truck18NMC811_EFORCE,Truck18FCNMC811_Daimler]                               # 18 t


############################################################
prodAndRecOffset = 2
vehiclesYearlyGWP100peryear = np.zeros((prodAndRecOffset+lifetime,len(vehicles)))
vehiclesGWP100ProTkm = np.zeros((prodAndRecOffset+lifetime,len(vehicles)))
# vehiclesYearlyGWP100peryear = np.zeros((1+lifetime,len(vehicles)))
# vehiclesGWP100ProTkm = np.zeros((1+lifetime,len(vehicles)))
columns = []
index = [2021]
names = []

n = 0

vehicleProdGWP100 = np.zeros((len(vehicles)))
vehicleRecGWP100 = np.zeros((len(vehicles)))
vehicleUsePhaseGWP100 = np.zeros((len(vehicles)))
endeIt = len(vehiclesYearlyGWP100peryear)
for vehicle in vehicles:
    columns.append(vehicle.name)
    names.append(vehicle.name)
    b = 0 # for pas km
    for i in range(0,endeIt):
        index.append(index[-1]+1)
        # calculate for production 0th year
        if i == 0:
            if vehicle.fcLeistung != 0:
                vehiclesYearlyGWP100peryear[i][n] = vehicle.cell.prodGWP100 + vehicle.fuelcellstack.prodGWP100 + vehicle.h2Tank.prodGWP100 # sum of cell prod + FC prod and H2 tank prod
                vehicleProdGWP100[n] = vehicle.cell.prodGWP100 + vehicle.fuelcellstack.prodGWP100 + vehicle.h2Tank.prodGWP100               # sum of cell prod + FC prod and H2 tank prod
            else:
                vehiclesYearlyGWP100peryear[i][n] = vehicle.cell.prodGWP100
                vehicleProdGWP100[n] = vehicle.cell.prodGWP100
        
        # calculate recycling at the EoL
        elif i == endeIt-1:
            if vehicle.fcLeistung != 0:
                vehicleRecGWP100[n] = vehicleRecGWP100[n] + vehicle.cell.recyclingHydroGWP100 + vehicle.fuelcellstack.recyclingHydroGWP100 + vehicle.h2Tank.recyclingHydroGWP100
                vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + vehicle.cell.recyclingHydroGWP100 + vehicle.fuelcellstack.recyclingHydroGWP100 + vehicle.h2Tank.recyclingHydroGWP100
            else:
                vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + vehicle.cell.recyclingHydroGWP100
                vehicleRecGWP100[n] = vehicleRecGWP100[n] + vehicle.cell.recyclingHydroGWP100 
        
        # calculate for use phase
        else:
            if i == vehicle.regulaererWechselzyklus:        # batterie wechselzyklen mitbetrachten
                if vehicle.fcLeistung != 0: # inlcuding the recycling of old Battery and new battery production
                    vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + ((h2Interpolation[i]*vehicle.consumption*vehicle.laufLeistungProJahr)/100) + vehicle.cell.prodGWP100 + vehicle.cell.recyclingHydroGWP100
                    vehicleRecGWP100[n] = vehicleRecGWP100[n] + vehicle.cell.recyclingHydroGWP100
                    # print(vehicleRecGWP100[n]) 
                    vehicleProdGWP100[n] = vehicleProdGWP100[n] + vehicle.cell.prodGWP100
                    # print(vehicleProdGWP100[n])
                    vehicleUsePhaseGWP100[n] = vehicleUsePhaseGWP100[n] + ((h2Interpolation[i]*vehicle.consumption*vehicle.laufLeistungProJahr)/100)
                    # print(vehicleUsePhaseGWP100[n])
                else:
                    vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + ((electricityInterpolation[i]*vehicle.consumption*vehicle.laufLeistungProJahr)/100) + vehicle.cell.prodGWP100 + vehicle.cell.recyclingHydroGWP100
                    vehicleRecGWP100[n] = vehicleRecGWP100[n] + vehicle.cell.recyclingHydroGWP100
                    vehicleProdGWP100[n] = vehicleProdGWP100[n] + vehicle.cell.prodGWP100
                    vehicleUsePhaseGWP100[n] = vehicleUsePhaseGWP100[n] +  ((electricityInterpolation[i]*vehicle.consumption*vehicle.laufLeistungProJahr)/100)
                    
            elif vehicle.fcLeistung != 0:
                    vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + ((h2Interpolation[i] * vehicle.consumption*vehicle.laufLeistungProJahr)/100)
                    vehicleUsePhaseGWP100[n] = vehicleUsePhaseGWP100[n] + ((h2Interpolation[i] * vehicle.consumption * vehicle.laufLeistungProJahr)/100)
            else:
                vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + ((electricityInterpolation[i]*vehicle.consumption*vehicle.laufLeistungProJahr)/100)
                vehicleUsePhaseGWP100[n] = vehicleUsePhaseGWP100[n] +  ((electricityInterpolation[i] * vehicle.consumption*vehicle.laufLeistungProJahr)/100)
        
        # calculate pro ton km
        gwp100perTkm = vehiclesYearlyGWP100peryear[i][n]/(vehicle.laufLeistungProJahr*b*vehicle.payload)
        vehiclesGWP100ProTkm[i][n] = gwp100perTkm
        b = b + 1
    n = n + 1

# create plot
fig, upDownPlot = plt.subplots()
# scale to tonnes
vehiclesYearlyGWP100peryearInTonnes = np.multiply(vehiclesYearlyGWP100peryear, 1E-3)
i = 0
linestyleDef = ['solid', 'dotted', 'dashed']
timeline = np.linspace(0,endeIt,14)
colors = plt.cm.jet(np.linspace(0,1,5))
for i in range(0, len(names)):
    # get payload class 
    plClass = names[i]
    plClass = plClass[:2]
    if plClass == '40': linestyleDefUse = linestyleDef[0]
    elif plClass == '25': linestyleDefUse = linestyleDef[1]
    elif plClass == '18': linestyleDefUse = linestyleDef[2]

    vehiclen = names[i]
    vehiclen = vehiclen[-4:]
    if vehiclen == ' 100': colorDefUse = colors[0] #'b'
    elif vehiclen == 'B 72': colorDefUse = colors[1] #'y'
    elif vehiclen == 'ORCE': colorDefUse = colors[2] #'g'
    elif vehiclen == 'mler': colorDefUse = colors[3] #'r'
    elif vehiclen == 'r ER': colorDefUse = colors[4] # 'b'
       
    toplot = np.array((vehiclesYearlyGWP100peryearInTonnes[:,i]))
    upDownPlot.plot(timeline, toplot, linestyle = linestyleDefUse, color = colorDefUse)

# upDownPlot.plot(vehiclesYearlyGWP100peryearInTonnes)

upDownPlot.legend(names)
upDownPlot.set_xlim(0, endeIt)
# plt.ylim(0, lifetime)
upDownPlot.set_xlabel("Years in Utilization")
upDownPlot.set_ylabel('GWP 100 in t CO$_2$ eq.')
#upDownPlot.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
#upDownPlot.grid()
plt.savefig(savepath + 'TrucksGWP100_UsePhase.pdf', format = 'pdf')

#### prepare data for bar chart
labels = names
ledgend = [ 'Recycling','Production', 'Use Phase']

# scale to tonnes
vehicleRecGWP100Scaled = np.multiply(vehicleRecGWP100, 1E-3)
vehicleProdGWP100Scaled = np.multiply(vehicleProdGWP100, 1E-3)
vehicleUsePhaseGWP100Scaled = np.multiply(vehicleUsePhaseGWP100, 1E-3)


valuesPlot = np.array([vehicleRecGWP100, vehicleProdGWP100, vehicleUsePhaseGWP100])
print(valuesPlot)
valuesPlotScaled = np.array([vehicleRecGWP100Scaled, vehicleProdGWP100Scaled, vehicleUsePhaseGWP100Scaled])
width = 0.3
data_shape = np.shape(valuesPlotScaled)
print(valuesPlotScaled)
# Take negative and positive data apart and cumulate
def get_cumulated_array(data, **kwargs):
    cum = data.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(data))
    d[1:] = cum[:-1]
    return d  

cumulated_data = get_cumulated_array(valuesPlotScaled, min=0)
cumulated_data_neg = get_cumulated_array(valuesPlotScaled, max=0)

# Re-merge negative and positive data.
row_mask = (valuesPlotScaled<0)
cumulated_data[row_mask] = cumulated_data_neg[row_mask]
data_stack = cumulated_data
print(data_stack)

#### https://medium.com/dunder-data/automatically-wrap-graph-labels-in-matplotlib-and-seaborn-a48740bc9ce
# text wrap for legend 
def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_xticklabels():
        text = label.get_text()
        labels.append(textwrap.fill(text, width=width,
                      break_long_words=break_long_words))
    ax.set_xticklabels(labels, rotation=0)

# plot bar
fig, barPlot = plt.subplots()
for i in range(valuesPlotScaled.shape[0]):
  barPlot.bar(labels, valuesPlotScaled[i], bottom=data_stack[i])    # bottom = np.sum(valuesPlotScaled[:i], axis = 0)

barPlot.set_ylabel('GWP 100 in kg CO$_2$ eq.')
# upDownPlot[1].label_outer()
barPlot.set_xticklabels(barPlot.get_xticklabels(), rotation=90)
# wrap_labels(upDownPlot[1], 5)
barPlot.legend(ledgend, fancybox=True, framealpha=0.5)
# barPlot.grid()
plt.rcParams['figure.figsize'] = [4, 4]
plt.savefig(savepath + 'TrucksGWP100_UsePhaseBar.pdf', format = 'pdf')
plt.show()


df1 = pd.DataFrame(vehiclesYearlyGWP100peryear)
df2 = pd.DataFrame(vehiclesGWP100ProTkm)

#df1.to_excel(savepath+"Trucks_Results.xlsx",index=index, header=columns) 
#df2.to_excel(savepath+"Trucks_Results_tkm.xlsx",index=index, header=columns)
df3 = pd.DataFrame(vehicleProdGWP100)
df4 = pd.DataFrame(vehicleRecGWP100)
df5 = pd.DataFrame(vehicleUsePhaseGWP100)

np.savetxt(savepath+"Trucks_production.txt", vehicleProdGWP100, fmt='%10.2f')
np.savetxt(savepath+"Trucks_recycling.txt", vehicleRecGWP100, fmt='%10.2f')
np.savetxt(savepath+"Trucks_UsePhase.txt", vehicleUsePhaseGWP100, fmt='%10.2f')
np.savetxt(savepath+"Trucks_Tkm.txt", vehiclesGWP100ProTkm, fmt='%10.5f')


############################################################
