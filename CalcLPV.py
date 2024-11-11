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

filename = "LPV_Results_mitMercedes"
savepath = r'C:\Users\shypo\Documents\Shared\01_Paper-Projekt-LCA-PEMFC\04-Plots\LVP\\'#'C:\Users\Leonard\tubCloud2\00_Uni\01_Paper-Projekt-LCA-PEMFC\04-Plots\LVP\\' #'C:\Users\Mein\tubCloud\00_Uni\01_Paper-Projekt-LCA-PEMFC\04-Plots\LVP\\'
# vehicle standards, lifetime in years, kmPerYear in km
lifetime = 12
kmPerYear = 15000

# set e-mix
## Germany
electricity2021Gemany = 0.475                       # kg CO2 /kWh
electricity2050Germany = 0.175                       # kg CO2 /kWh

## EU
electricity2021EU = 0.427                       # kg CO2 /kWh
electricity2050EU = 0.12100                       # kg CO2 /kWh

electricityInterpolation = np.linspace(electricity2021Gemany,electricity2050Germany,50-21)


h2Prod2021 = 15.37125                           # kg CO2 / kWh
h2Prod2050 = 6.45773                           # kg CO2 / kWh

h2Interpolation = np.linspace(h2Prod2021,h2Prod2050,50-21)

plt.plot(h2Interpolation)
plt.show()


toyotaMirai2 = LPV('Toyota Mirai 2', kmPerYear, lifetime,'NMC811',  batteryCap=0.95, passengers = 1, consumption = 0.84, vehrange = 650, fcLeistung = 128, h2Cap=5)
hyundaiNexus = LPV('Hyundai Nexo', kmPerYear, lifetime, 'NMC811', batteryCap=1.56, passengers = 1, consumption = 0.95, vehrange = 666, fcLeistung = 95, h2Cap=5)
volkswagenID3 = LPV('VW ID.3', kmPerYear, lifetime, 'NMC811', 62, passengers = 1, consumption = 15.5, vehrange = 426, fcLeistung = 0, h2Cap=0)
volkswagenID4 = LPV('VW ID.4', kmPerYear, lifetime, 'NMC811', 55, passengers = 1, consumption = 16.7, vehrange = 346, fcLeistung = 0, h2Cap=0)
# with comparable range
mercedesEQS580 = LPV('Mercedes Benz EQS 580 4Matic', kmPerYear, lifetime, 'NMC811', 120, passengers = 1, consumption = 17.7, vehrange = 672, fcLeistung = 0, h2Cap=0)

# create list with vehicles --> add vehicles to the list, if added
vehicles = [toyotaMirai2,hyundaiNexus,
            volkswagenID3,volkswagenID4,mercedesEQS580]

# list of vehicles
vehiclesYearlyGWP100perPassenger = np.zeros((lifetime,len(vehicles)))
columns = []
index = [2021]
names = []

n = 0   

# begin
#############################

# set vehicle list to run loop over vehicles (Add the vehicles to investigate)
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
            if vehicle.fcLeistung != 0:
                    vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + ((h2Interpolation[i] * vehicle.consumption*vehicle.laufLeistungProJahr)/100)
                    vehicleUsePhaseGWP100[n] = vehicleUsePhaseGWP100[n] + ((h2Interpolation[i] * vehicle.consumption * vehicle.laufLeistungProJahr)/100)
            else:
                vehiclesYearlyGWP100peryear[i][n] = vehiclesYearlyGWP100peryear[i-1][n] + ((electricityInterpolation[i] * vehicle.consumption * vehicle.laufLeistungProJahr)/100)
                vehicleUsePhaseGWP100[n] = vehicleUsePhaseGWP100[n] +  ((electricityInterpolation[i] * vehicle.consumption * vehicle.laufLeistungProJahr)/100)
        
        # calculate pro ton km
        gwp100Propassengerkm = vehiclesYearlyGWP100peryear[i][n]/(vehicle.laufLeistungProJahr*b*vehicle.passengers)
        vehiclesGWP100ProPassengerkm[i][n] = gwp100Propassengerkm
        b = b + 1
    n = n + 1

# create plot
fig, upDownPlot = plt.subplots(2)
upDownPlot[0].plot(np.multiply(vehiclesYearlyGWP100peryear, 1E-3))

upDownPlot[0].legend(names)
upDownPlot[0].set_xlim(0, lifetime)
# plt.ylim(0, lifetime)
upDownPlot[0].set_xlabel("Years in Utilization")
upDownPlot[0].set_ylabel('GWP 100 in t CO$_2$ eq.')
upDownPlot[0].tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
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
  upDownPlot[1].bar(labels, valuesPlotScaled[i], bottom=data_stack[i]) # bottom = np.sum(valuesPlotScaled[:i], axis = 0)

# bars.set_ylabel('GWP 100 in kg CO$_2$ eq.')
upDownPlot[1].label_outer()
wrap_labels(upDownPlot[1], 7)
upDownPlot[1].legend(ledgend, fancybox=True, framealpha=0.5)
upDownPlot[0].grid()
upDownPlot[1].grid()
plt.savefig(savepath + 'LPVsGWP100_UsePhase.pdf', format = 'pdf')




# create data frame to save values
df1 = pd.DataFrame(vehiclesYearlyGWP100peryear)
df3 = pd.DataFrame(vehicleProdGWP100)
df4 = pd.DataFrame(vehicleRecGWP100)
df5 = pd.DataFrame(vehicleUsePhaseGWP100)



#df1.to_excel(savepath+"LPV_Results.xlsx",index=index, header=columns) 
# df2.to_excel(savepath+"LPV_Results_Pkm.xlsx",index=index, header=columns)
# df3.to_excel(savepath+"LPV_recycling.xlsx",index=[1], header=columns)
np.savetxt(savepath+"LPV_production.txt", vehicleProdGWP100, fmt='%10.2f')
np.savetxt(savepath+"LPV_recycling.txt", vehicleRecGWP100, fmt='%10.2f')
np.savetxt(savepath+"LPV_Usephase.txt", vehicleUsePhaseGWP100, fmt='%10.2f')

#############################

