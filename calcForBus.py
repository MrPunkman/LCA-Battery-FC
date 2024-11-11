'''Calc for Bus systems'''

from timeit import default_timer as timer
from openlca_automation.tool import lca
import gradio as gr
import olca
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from vehicleDef import *
from oLCAInventory import *
from energyMixDef import *
import textwrap


savepath = r'C:\Users\Mein\tubCloud\00_Uni\01_Paper-Projekt-LCA-PEMFC\04-Plots\Bus\\'
# vehicle standards, lifetime in years, kmPerYear in km
lifetime = 12
kmPerYear = 60000

# set e-mix
## Germany
electricity2021Gemany = 0.475                       # kg CO2 /kWh
electricity2050Germany = 0.175                       # kg CO2 /kWh

## EU
electricity2021EU = 0.427                       # kg CO2 /kWh
electricity2050EU = 0.12100                       # kg CO2 /kWh


# linear interpolation of the energy mix and hydrogen data
electricityInterpolation = np.linspace(electricity2021EU,electricity2050EU,50-21)

h2Prod2021 = 15.37125                           # kg CO2 / kg
h2Prod2050 = 6.45773                           # kg CO2 / kg

h2Interpolation = np.linspace(h2Prod2021,h2Prod2050,50-21)

# meinEnergieMixEAuto = EnergyMix(nuclear=3.98, geothermal=0.03,rbiomass=7.72, coal=15.25,wind=39.35,solar=25.39,water=1.9,pump=9.05,gas=5.09,oil=0.01)
# meinEnergieMixFCAuto = EnergyMix(nuclear=3.98, geothermal=0.03,rbiomass=7.72, coal=15.25,wind=39.35,solar=25.39,water=1.9,pump=9.05,gas=5.09,oil=0.01)

# define busses for investigation
bus12FCNMC811_70_31 =   Bus(name = "12 m FC 70 B 31",passengers = 75, laufLeistungProJahr = kmPerYear,cellchem='NMC811', lebensDauer = lifetime, batteryCap = 31, consumption = 8.5, fcLeistung = 70, h2Cap = 40)
bus12NMC811_300 =       Bus(name = "12 m B 300",passengers= 85, laufLeistungProJahr = kmPerYear,cellchem='NMC811', lebensDauer = lifetime, batteryCap = 300, vehrange = 285, consumption = 335, fcLeistung = 0, h2Cap=0)
bus12NMC811_90 =        Bus(name = "12 m B 90",passengers= 100, laufLeistungProJahr = kmPerYear,cellchem='NMC811', lebensDauer = lifetime, batteryCap = 90,vehrange = 260, consumption = 300, fcLeistung = 0, h2Cap=0)
# names = ["FC 70 B 31 12 m","B 300 12 m", "B 90 12 m"] # needed for legend

# set vehicle list to run loop over vehicles (Add the vehicles to investigate)
vehicles = [bus12FCNMC811_70_31, bus12NMC811_300, bus12NMC811_90]
# year 0 is production, year life + 1 is recycling, battery exchange cycle
prodAndRecOffset = 2
vehiclesYearlyGWP100peryear = np.zeros((prodAndRecOffset+lifetime,len(vehicles)))
vehiclesGWP100ProPassengerkm = np.zeros((prodAndRecOffset+lifetime,len(vehicles)))
columns = []
index = [2021]
names = []

n = 0
b = 1 # for pas km
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
        gwp100Propassengerkm = vehiclesYearlyGWP100peryear[i][n]/(vehicle.laufLeistungProJahr*b*vehicle.passengers*vehicle.realpassengers*0.01)
        vehiclesGWP100ProPassengerkm[i][n] = gwp100Propassengerkm
        b = b + 1
    n = n + 1

# create plot
fig, (usephase, bars) = plt.subplots(1,2)
usephase.plot(np.multiply(vehiclesYearlyGWP100peryear, 1E-3))
usephase.legend(names)
usephase.set_xlim(0, 12)
# plt.ylim(0, lifetime)
usephase.set_xlabel("Years in Utilization")
usephase.set_ylabel('GWP 100 in t CO$_2$ eq.')

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
for i in range(valuesPlotScaled.shape[0]):
  bars.bar(labels, valuesPlotScaled[i], bottom=data_stack[i]) # bottom = np.sum(valuesPlotScaled[:i], axis = 0)

# bars.set_ylabel('GWP 100 in kg CO$_2$ eq.')
bars.label_outer()
wrap_labels(bars, 5)
# plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
bars.legend(ledgend, bbox_to_anchor=(0.3, 1.1), fancybox=True, framealpha=0.5,  loc = "upper center", ncol= n) #
usephase.grid()
# bars.grid()
plt.savefig(savepath + 'BusesGWP100_UsePhase.pdf', format = 'pdf')
plt.show()


# create data frame to save values
df1 = pd.DataFrame(vehiclesYearlyGWP100peryear)
df2 = pd.DataFrame(vehiclesGWP100ProPassengerkm)
df3 = pd.DataFrame(vehicleProdGWP100)
df4 = pd.DataFrame(vehicleRecGWP100)
df5 = pd.DataFrame(vehicleUsePhaseGWP100)


#df1.to_excel(savepath+"Bus_Results.xlsx",index=index, header=columns) 
#df2.to_excel(savepath+"Bus_Results_Pkm.xlsx",index=index, header=columns)
# df3.to_excel(savepath+"Bus_recycling.xlsx",index=[1], header=columns)
np.savetxt(savepath+"Bus_production.txt", vehicleProdGWP100, fmt='%10.2f')
np.savetxt(savepath+"Bus_recycling.txt", vehicleRecGWP100, fmt='%10.2f')
np.savetxt(savepath+"Bus_UsePhase.txt", vehicleUsePhaseGWP100, fmt='%10.2f')
np.savetxt(savepath+"Bus_PasKM.txt", vehiclesGWP100ProPassengerkm, fmt='%10.5f')



