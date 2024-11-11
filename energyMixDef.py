'''This class can be extended for automized calculation of Hydrogen and Energy production'''
from timeit import default_timer as timer
from openlca_automation.tool import lca
#import gradio as gr
import olca
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from vehicleDef import *
from fuelCellDef import *
from oLCAInventory import *
from batteryDef import *


class HydrogenMix:
    def __init__(self, name, overall):
        self.name = name
        self.overall = overall

class EnergyMix:
    def __init__(self, name, overall=0, pump = 10, solar=10, wind=10, rbiomass=10, geothermal=10,water = 10, coal=10, gas=10, nuclear=20, oil=20):
        self.name = name
        if overall != 0:
            self.foodprint = overall
        else:
            self.wind           = wind/100
            self.solar          = solar/100
            self.rbiomass       = rbiomass/100
            self.geothermal     = geothermal/100
            self.coal           = coal/100
            self.gas            = gas/100
            self.nuclear        = nuclear/100
            self.oil            = oil/100
            self.water          = water/100
            self.pump           = pump/100
            self.foodprint = self.water * self.fwater + self.solar * self.fPsolar + self.wind * self.fPwind + self.rbiomass*self.fPrbiomass + self.geothermal*self.fPgeothermal + self.coal*self.fPcoal+ self.gas*self.fPgas+ self.nuclear*self.fPnuclear + self.oil * self.fOil
    fPwind           = 0.013
    fPsolar          = 0.035
    fPrbiomass       = 0.230
    fPgeothermal     = 0.038
    fPcoal           = 1.152
    fPgas            = 0.661
    fPnuclear        = 0.005
    fOil             = 1.125
    fwater           = 0.011
    fpump            = 0.419


    
    def calcCO2forEnergymix(self):
        foodprint = self.solar * self.fPsolar + self.wind * self.fPwind + self.rbiomass*self.fPrbiomass + self.geothermal*self.fPgeothermal + self.coal*self.fPcoal+ self.gas*self.fPgas+ self.nuclear*self.fPnuclear + self.nrbiomass * self.fPnrbiomass
        print('Your Energymix causes:%.4f' %foodprint, 'kg CO2 eq/kWh')
        return

