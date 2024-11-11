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
#class Vehicle():
    # def __init__(self, laufLeistungProJahr, lebensDauer,  batteryCap, consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
   
        

class Truck():
    BOPweightPerKW = 85.274/80 # weight of BOP
    def __init__(self, name, gvW, laufLeistungProJahr, lebensDauer,cellchem,  batteryCap, payloadfactor, consumption=0, vehrange=0, fcLeistung = 0, h2Cap=0, payload=0):
        self.name = name
        self.fcLifehours = 20000
        self.ladezyklen = 4000
        self.regulaererWechselzyklus = 6
        self.usedSOC = 0.8
        self.laufLeistungProJahr = laufLeistungProJahr
        self.lebensDauer = lebensDauer
        self.fcLeistung = fcLeistung
        self.batteryCap = batteryCap
        self.h2energyDensity = 33.3
        self.cellchem = cellchem
        self.BOPweight = Truck.BOPweightPerKW * self.fcLeistung 
        self.h2Cap = h2Cap
        self.payloadfactor = payloadfactor

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
        
        # calc for payload the emptyweight of the truck without power train
        self.emptyNoPowerSystem = self.motor + self.eSystem + self.chassisFrame + self.suspension + self.brakingSystem + self.wheels + self.cabin + self.body + self.other


        # create battery
        self.cell = Batterie(self.cellchem,self.batteryCap)

        # calc values for FC Truck
        if fcLeistung != 0:
            self.h2Tank = HydrogenTankSystem('Hydrogen Tank',kgHydrogen=self.h2Cap)
            self.fuelCell = FuelCell('FC')
            self.fuelcellstack = FuelCellStack('FC',power = self.fcLeistung)
            self.weightPowersystemcell = self.cell.weightofBattery + self.fuelcellstack.weight +self.h2Tank.weight + self.BOPweight
            self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus
            if payload == 0:
                self.payload = self.payloadfactor * (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
            else:
                self.payload = payload

        # calculate consumption - send message, if consumption && range are 0 !
            if consumption and vehrange != 0:
                self.vehrange = vehrange
                self.consumption = consumption 
            elif vehrange == 0:
                self.consumption = consumption
                self.vehrange = 100 * (self.h2Cap /self.consumption)
            elif consumption == 0:
                self.vehrange = vehrange
                self.consumption = self.h2Cap/(self.vehrange)*100
            else: print('set consumption or range!!')

    
        # Calc values for pure battery truck
        else:
            self.weightPowersystemcell = self.cell.weightofBattery
            self.payload = (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
            self.payload = self.payload/2

            if consumption and vehrange != 0:
                self.vehrange = vehrange
                self.consumption = consumption
                
            elif vehrange == 0:
                self.consumption = consumption
                self.vehrange = (self.batteryCap * self.usedSOC /self.consumption)*100

            elif consumption == 0:
                self.vehrange = vehrange
                self.consumption = self.batteryCap/(self.vehrange)*100
            else:
                print('set consumption or range != 0 !!')

        # calc cylces per year
        self.jahreszyklen = laufLeistungProJahr/self.vehrange
        self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus
        
        # self.payload = (1000* self.gvW-(self.emptyNoPowerSystem + self.weightPowersystemcell))/1000
        # print(self.payload)


# class for Busses
class Bus:
    BOPweightPerKW = 85.274/80
    
    def __init__(self, name, passengers, laufLeistungProJahr, lebensDauer,cellchem,  batteryCap, avPassengerOcc = 65 ,consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
        self.name = name
        self.fcLifehours = 20000
        self.ladezyklen = 4000
        self.regulaererWechselzyklus = 6
        self.usedSOC = 0.8
        self.laufLeistungProJahr = laufLeistungProJahr
        self.lebensDauer = lebensDauer
        self.fcLeistung = fcLeistung
        self.batteryCap = batteryCap
        self.h2energyDensity = 33.3
        self.cellchem = cellchem
        self.BOPweight = Truck.BOPweightPerKW * self.fcLeistung 
        self.h2Cap = h2Cap
        self.vehrange = vehrange
        self.consumption = consumption
        self.realpassengers = avPassengerOcc

    # define vehicles assemblies weights in kg
        self.passengers = passengers

        
        self.cell = Batterie(self.cellchem,self.batteryCap)

        
        if fcLeistung != 0:
            self.fuelCell = FuelCell('FC')
            self.fuelcellstack = FuelCellStack('FC',power = self.fcLeistung)
            self.h2Tank = HydrogenTankSystem('Hydrogen Tank',kgHydrogen = self.h2Cap)
            self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus

            # if consumption and vehrange == 0:
            #     print('set consumption or range!!')
            if vehrange == 0:
                self.consumption = consumption
                self.vehrange = 100*(self.h2Cap /(self.consumption))
            elif consumption == 0:
                self.consumption = self.h2Cap/(self.vehrange)*100
                self.vehrange = vehrange
            else: print('set consumption or range!!')
    

        else:
            self.weightPowersystemcell = self.cell.weightofBattery
            if consumption and vehrange == 0:
                print('set consumption or range != 0 !!')
            
            elif vehrange == 0: 
                self.vehrange = self.batteryCap * self.usedSOC /(100*consumption)
                self.consumption = consumption
            elif consumption == 0: 
                self.consumption = self.batteryCap/(self.vehrange)*100
                self.vehrange = vehrange

            else: pass

            self.jahreszyklen = laufLeistungProJahr/self.vehrange
            self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus


class LPV:
    BOPweightPerKW = 85.274/80
    def __init__(self, name, laufLeistungProJahr, lebensDauer, cellchem, batteryCap, passengers = 1.42, consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
        self.passengers = passengers
        self.name = name
        self.fcLifehours = 7000
        self.ladezyklen = 4000
        #self.regulaererWechselzyklus = 6
        self.usedSOC = 0.8
        self.laufLeistungProJahr = laufLeistungProJahr
        self.lebensDauer = lebensDauer
        self.fcLeistung = fcLeistung
        self.batteryCap = batteryCap
        self.h2energyDensity = 33.6
        self.cellchem = cellchem
        self.BOPweight = Truck.BOPweightPerKW * self.fcLeistung 
        self.h2Cap = h2Cap

       
        self.cell = Batterie(self.cellchem,self.batteryCap)

        
        self.consumption = consumption
     
        self.vehrange = vehrange
        

        # do that if FCEV !
        if fcLeistung != 0:
            self.fuelCell = FuelCell('FC')
            self.fuelcellstack = FuelCellStack('FC',power = self.fcLeistung)
            self.h2Tank = HydrogenTankSystem('Hydrogen Tank',kgHydrogen=self.h2Cap)
            self.weightPowersystemcell = self.cell.weightofBattery + self.fuelcellstack.weight +self.h2Tank.weight + self.BOPweight
            #self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus
 # if consumption and vehrange == 0:
            #     print('set consumption or range!!')
            if vehrange == 0:
                self.consumption = consumption
                self.vehrange = 100*(self.h2Cap /(self.consumption))
            elif consumption == 0:
                self.consumption = self.h2Cap/(self.vehrange)*100
                self.vehrange = vehrange
            else: print('set consumption or range!!')
    

        else:
            self.weightPowersystemcell = self.cell.weightofBattery
            if consumption and vehrange == 0:
                print('set consumption or range != 0 !!')
            
            elif vehrange == 0: 
                self.vehrange = self.batteryCap * self.usedSOC /(100*consumption)
                self.consumption = consumption
            elif consumption == 0: 
                self.consumption = self.batteryCap/(self.vehrange)*100
                self.vehrange = vehrange

            else: pass
            
        
class Train:
    BOPweightPerKW = 85.274/80
    
    def __init__(self, name, passengers, laufLeistungProJahr, lebensDauer,cellchem,  batteryCap, avPassengerOcc = 50,consumption = 0, vehrange = 0, fcLeistung = 0, h2Cap=0):
        self.name = name
        self.fcLifehours = 20000
        self.ladezyklen = 4000
        self.regulaererWechselzyklus = 6
        self.usedSOC = 0.8
        self.laufLeistungProJahr = laufLeistungProJahr
        self.lebensDauer = lebensDauer
        self.fcLeistung = fcLeistung
        self.batteryCap = batteryCap
        self.h2energyDensity = 33.3
        self.cellchem = cellchem
        self.BOPweight = Truck.BOPweightPerKW * self.fcLeistung 
        self.h2Cap = h2Cap

    # define vehicles assemblies weights in kg
        self.passengers = passengers

        
        self.cell = Batterie(self.cellchem,self.batteryCap)

        self.consumption = consumption
        self.vehrange = vehrange

        
        if fcLeistung != 0:
            self.fuelCell = FuelCell('FC')
            self.fuelcellstack = FuelCellStack('FC',power = self.fcLeistung)
            self.h2Tank = HydrogenTankSystem('Hydrogen Tank',kgHydrogen=self.h2Cap)
            # self.weightPowersystemcell = self.cell.weightofBattery + self.fuelcellstack.weight +self.h2Tank.weight + self.BOPweight
            self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus

            if self.consumption and self.vehrange == 0:
                print('set consumption or range!!')
            else:
                if self.vehrange == 0:
                    self.vegrange = self.batteryCap * self.usedSOC /(100*self.consumption)
                else:
                    self.consumption = self.batteryCap/(self.vehrange)*100
    

        else:
            self.weightPowersystemcell = self.cell.weightofBattery
            if self.consumption and self.vehrange == 0:
                print('set consumption or range != 0 !!')
            
            elif vehrange == 0:
                self.vehrange = self.batteryCap * self.usedSOC /(100*consumption)

            else:
                self.consumption = self.batteryCap/(self.vehrange)*100

            self.jahreszyklen = laufLeistungProJahr/self.vehrange
            self.amountOfBatteries = lebensDauer//self.regulaererWechselzyklus

