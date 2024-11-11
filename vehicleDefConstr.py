# in case, you don't have the .csv data, create new batteries/cellchemistries and run the following lines depending on the system you need the csv data
    # cellNMC811.calcProdAndRecyclingCED()
    # cellNMC111.calcProdAndRecyclingCED()
    # cellNCA.calcProdAndRecyclingCED()
    # cellLFP.calcProdAndRecyclingCED()
    # kWFuelcell.calcProdAndRecyclingCED()
    # fuelCell.calcProdAndRecyclingCED()

    # cellNMC811.calcProdAndRecyclingReCePi2016()
    # cellNMC111.calcProdAndRecyclingReCePi2016()
    # cellNCA.calcProdAndRecyclingReCePi2016()
    # cellLFP.calcProdAndRecyclingReCePi2016()
    # kWFuelcell.calcProdAndRecyclingReCePi2016()
    # fuelCell.calcProdAndRecyclingReCePi2016()

# this file contains the classes for the vehicles 
# and subclasses too build a vehicle drivetrain


# every class returns its GWP, HTPc, CED, AED and SOP

# class for cell chemistries
from timeit import default_timer as timer
from fuelCellDef import FuelCell, FuelCellStack, HydrogenTankSystem
from openlca_automation.tool import lca
import gradio as gr
import olca
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from vehicleDef import *
from fuelCellDef import *
from oLCAInventory import *
from batteryDef import *


# ---------------------------------------------------------------------------------------------------------
# create drivetrains

# class BEDirvetrain:
#     def __init__(self, gBattery, gEnginePower):
#         self.battery        = gBattery
#         self.EnginePower    = gEnginePower


# class H2Drivetrain:
#     def __init__(self, gBattery, gFCStack, gNStacks, gEnginePower, gHydrogenTank):
#         self.battery        = gBattery
#         self.FCStack        = gFCStack
#         self.nStacks        = gNStacks
#         self.EnginePower    = gEnginePower
#         self.hydrogenTank   = gHydrogenTank
        

# ---------------------------------------------------------------------------------------------------------        
# create vehicles
# values in km, years, kWh, (kg/kW)/100 km, km, kW, kg
# Batterie,H2Drivetrain
class Vehicle():
    BOPweightPerKW = 85.274/80
    def __init__(self, name, laufLeistungProJahr, lebensDauer, cellchem,  batteryCap, consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
        self.name = name
        self.usedSOC = 0.8
        self.laufLeistungProJahr = laufLeistungProJahr
        self.ladezyklen = 4000
        self.lebensDauer = lebensDauer
        self.fcLeistung = fcLeistung
        self.batteryCap = batteryCap
        self.h2energyDensity = 33.6
        self.cellchem = cellchem
        self.BOPweight = Vehicle.BOPweightPerKW * self.fcLeistung 
        self.h2Cap = h2Cap

        # create battery and hydrogen tank system
        self.cell = Batterie(self.cellchem,self.batteryCap)

        self.h2Tank = HydrogenTankSystem('Hydrogen Tank',kgHydrogen=self.h2Cap)

        # calculate kgH2/100 km to kWh/100 km
        if fcLeistung != 0:
            self.consumption = consumption * self.h2energyDensity
        else:
            self.consumption = consumption

        
        if fcLeistung != 0:
            self.fuelCell = FuelCell('FC')
            self.fuelcellstack = FuelCellStack('FC',power = self.fcLeistung)
            self.weightPowersystemFC = self.cell.weightofBattery + self.fuelcellstack.weight + self.h2Tank.weight + self.BOPweight
            self.amountOfBatteries = self.lebensDauer//self.regulaererWechselzyklus
            
            if self.consumption and vehrange != 0:
                print('set consumption or range!!')
            else:
                if vehrange == 0:
                    self.range = batteryCap * self.usedSOC /(100*consumption)
                else:
                    self.vehrange = vehrange
                    self.consumption = self.batteryCap/(vehrange)*100
    

        else:
            self.weightPowersystemFC = self.cell.weightofBattery
            self.payload = (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemFC))/1000
            self.payload = self.payload/2
            if consumption & vehrange != 0:
                print('set consumption or range != 0 !!')
            
            elif vehrange == 0:
                self.vehrange = batteryCap * self.usedSOC /(100*consumption)

            else:
                self.vehrange = vehrange
                self.consumption = self.batteryCap/(vehrange)*100

                self.jahreszyklen = laufLeistungProJahr/vehrange
                self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus
        
        

        


    



class Truck(Vehicle):
    
    def __init__(self, name, gvW, laufLeistungProJahr, lebensDauer,cellchem,  batteryCap, consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
        super().__init__(name,laufLeistungProJahr, lebensDauer,cellchem,  batteryCap, consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0)
        self.regulaererWechselzyklus = 6
        self.fcLifehours = 20000

    # define vehicles assemblies weights in kg
        self.gvW = gvW
        # self.AnneTruck18t= 10800
        # self.AnneDT = 450
        self.motor = 308
        self.eSystem = 265
        self.chassisFrame = 3439
        self.suspension = 2328
        self.brakingSystem = 784
        self.wheels = 1352
        self.cabin = 1153
        self.body = 2100
        self.other = 1158
        
        # Calculate empty power system with predefined values for the truck
        self.emptyNoPowerSystem = self.motor + self.eSystem + self.chassisFrame + self.suspension + self.brakingSystem + self.wheels + self.cabin + self.body + self.other
        
        if fcLeistung != 0:
            self.payload = (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
    

        else:
            self.weightPowersystemcell = self.cell.weightofBattery
            self.payload = (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
            self.payload = self.payload/2
            if consumption & vehrange != 0:
                print('set consumption or range != 0 !!')
            
            elif vehrange == 0:
                self.vehrange = batteryCap * self.usedSOC /(100*consumption)

            else:
                self.vehrange = vehrange
                self.consumption = self.batteryCap/(vehrange)*100

                self.jahreszyklen = laufLeistungProJahr/vehrange
                self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus

        

        

        
        # self.payload = (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
        

        # print(self.payload)

class Bus:
    def __init__(self, gLength, gOEM, gModell, usedRef, gGVW, gMaxPassenger, gMaxDis, gPowerTrain):
        self.legnth         = gLength
        self.oem            = gOEM
        self.modell         = gModell
        self.ref            = usedRef
        self.gvw            = gGVW
        self.maxPassenger   = gMaxPassenger
        self.distance       = gMaxDis
        self.powertrain     = gPowerTrain
        
    def print_Energystorage(self):
        print(self.energyType, self.capacity, self.fuelCellPower, self.tankWeight)


class LPV:
    BOPweightPerKW = 85.274/80
    def __init__(self, name, passengers,laufLeistungProJahr, lebensDauer,cellchem,  batteryCap, consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
        self.name = name
        self.fcLifehours = 7000
        self.ladezyklen = 4000
        self.regulaererWechselzyklus = 6
        self.usedSOC = 0.8
        self.laufLeistungProJahr = laufLeistungProJahr
        self.lebensDauer = lebensDauer
        self.fcLeistung = fcLeistung
        self.batteryCap = batteryCap
        self.h2energyDensity = 33.6
        self.cellchem = cellchem
        self.BOPweight = Truck.BOPweightPerKW * self.fcLeistung 
        self.h2Cap = h2Cap

    # define vehicles assemblies weights in kg
        self.passengers = passengers
        self.motor = 308
        self.eSystem = 265
        self.chassisFrame = 3439
        self.suspension = 2328
        self.brakingSystem = 784
        self.wheels = 1352
        self.cabin = 1153
        self.body = 2100
        self.other = 1158
        
        self.cell = Batterie(self.cellchem,self.batteryCap)

        self.h2Tank = HydrogenTankSystem('Hydrogen Tank',kgHydrogen=self.h2Cap)
        

        # calculate kgH2/100 km to kWh/100 km
        if fcLeistung != 0:
            self.consumption = consumption * self.h2energyDensity
        else:
            self.consumption = consumption

        
        if fcLeistung != 0:
            self.fuelCell = FuelCell('FC')
            self.fuelcellstack = FuelCellStack('FC',power = self.fcLeistung)
            self.weightPowersystemcell = self.cell.weightofBattery + self.fuelcellstack.weight +self.h2Tank.weight + self.BOPweight
            self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus
            self.payload = (1000* self.passengers*80-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
            if self.consumption and vehrange != 0:
                print('set consumption or range!!')
            else:
                if vehrange == 0:
                    self.range = batteryCap * self.usedSOC /(100*consumption)
                else:
                    self.vehrange = vehrange
                    self.consumption = self.batteryCap/(vehrange)*100
    

        else:
            self.payload = (1000* self.passengers*80-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
            self.payload = self.payload/2
            self.weightPowersystemcell = self.cell.weightofBattery
            if consumption & vehrange != 0:
                print('set consumption or range != 0 !!')
            
            elif vehrange == 0:
                self.vehrange = batteryCap * self.usedSOC /(100*consumption)

            else:
                self.vehrange = vehrange
                self.consumption = self.batteryCap/(vehrange)*100

                self.jahreszyklen = laufLeistungProJahr/vehrange
                self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus

        

        

        self.emptyNoPowerSystem = self.motor + self.eSystem + self.chassisFrame + self.suspension + self.brakingSystem + self.wheels + self.cabin + self.body + self.other
        
        


