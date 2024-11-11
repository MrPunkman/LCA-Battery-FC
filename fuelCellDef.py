# in case, you don't have the .csv data, create new batteries/cellchemistries and run the following lines depending on the system you need the csv data
    # cellNMC811.calcProdAndRecyclingCED()
    # cellNMC111.calcProdAndRecyclingCED()
    # cellNCA.calcProdAndRecyclingCED()
    # cellLFP.calcProdAndRecyclingCED()
    # fuelCell.calcProdAndRecyclingCED()
    # kWFuelcell.calcProdAndRecyclingCED()

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




class FuelCell:
# set typeFC to 'FC' or 'FC 80 kW' !!!
    def __init__(self, typeFC = 'FC 80 kW' or 'Hydrogen Tank' or 'FC'):
        self.name           = typeFC
        self.typeFC         = typeFC
        self.fcProdsystems  = 0

    # chose the right productsystems to create a FC
        if self.name == 'FC 80 kW':
            
            self.fcProdsystems = {"fc80kwprod" : '80 kW Fuel Cell System production',
                                "fcBPrec" : 'FC Bipolar Plates Recycling - v2',
                                "fcCCrec" : 'FC Current Collectors Recycling',
                                "fcEGrec" : 'FC End Gaskets Recycling',
                                "fcFMrec" : 'FC Fuel Management Recycling',
                                "fcGDLrec" : 'FC Gas Diffusion Layer Recycling',
                                "fcHMrec" : 'FC Heat Management Recycling',
                                "fcBOPothersrec" : 'FC Other BOP Recycling',
                                "fcEPrec" : 'FC Stack Endplates Recycling',
                                "fcSHrec" : 'FC Stack Housing Recycling',
                                "fcAMrec" : 'FC Air Management Recycling',
                                "fcStackCBrec" : "FC Stack compression bands Recycling",
                                "fcH2OMrec"  : 'FC Water Management Recycling',
                                }
        elif self.name == 'Hydrogen Tank':
            self.fcProdsystems = {"fcH2Tankprod" : 'FC Hydrogen tank production',
                                "fcH2Tankrec" : 'FC Hydrogen Tank Recycling-v2'
                                }
#
        elif self.name == 'FC':
            self.fcProdsystems = {"fckwprod" : '1 kW Fuel Cell System production',
                    "fcAMrec" : 'FC Air Management Recycling',
                    "fcBPrec" : 'FC Bipolar Plates Recycling',
                    "fcCCrec" : 'FC Current Collectors Recycling',
                    "fcEGrec" : 'FC End Gaskets Recycling',
                    "fcFMrec" : 'FC Fuel Management Recycling',
                    "fcGDLrec" : 'FC Gas Diffusion Layer Recycling',
                    "fcHMrec" : 'FC Heat Management Recycling',
                    "fcBOPothersrec" : 'FC Other BOP Recycling',
                    "fcEPrec" : 'FC Stack Endplates Recycling',
                    "fcSHrec" : 'FC Stack Housing Recycling',
                    "fcStackCBrec" : "FC Stack compression bands Recycling",
                    "fcH2OMrec"  : 'FC Water Management Recycling',
                    "PEMrec" :'proton exchange membrane recycling',
                    "Transportrec": "FC Recycling GREET Collection and Transportation EverBatt"     
                                }
            # self.fcProdsystems = {"fckwprod" : '1 kW Fuel Cell System production',
            #                     "fcAMrec" : 'FC Air Management Production',
            #                     "fcBPrec" : 'FC Bipolar Plates Production',
            #                     "fcCrec" : 'FC Catalyst Production',
            #                     "fcCCrec" : 'FC Current collectors Production',
            #                     "fcEGrec" : 'FC End gaskets Production',
            #                     "fcFMrec" : 'FC Fuel management Production',
            #                     "fcGDLrec" : 'FC Gas Diffusion Layer Production',
            #                     "fcHMrec" : 'FC Heat Management Production',
            #                     "fcHTrec" : "FC Hydrogen tank production",
            #                     "fcMEArec" : 'FC Membrane Electrode Assembley Production',
            #                     "fcMrec" : 'FC Membrane Production',
            #                     "fcBOPothersrec" : 'FC Other BOP Production',
            #                     "fctransrec" : 'FC Production transport',
            #                     "fcEPrec" : 'FC Stack Endplates Production',
            #                     "fcCBrec" : 'FC Stack compression bands Production',
            #                     "fcSHrec" : 'FC Stack housing Production',
            #                     "fcH2OMrec"  : 'FC Water Management Production'   
            #                     }


        else: print('Your System is not in the FC - list')


    ### Create outputs for a productsystem for variable impactmethode
    def calcCEDWithOpenLCA(self, productsystem, impactMethod):
        print(productsystem)
        client = olca.Client(8080)
        setup = olca.CalculationSetup()
        print("running openLCA...", end="\r")
        impact_categories = lca.openlca(impactMethod, productsystem, port=8080)    
        result = client.calculate(setup)
        client.excel_export(result, 'result.xlsx')

        df = pd.read_excel('result.xlsx', header=1, sheet_name='Impacts')
        df = df.fillna(0)

        cedOfLFP = np.array(df.iloc[:].Result)

        df = 0
        client.dispose(result)

        print("Done! You can find the results of "+ productsystem + impactMethod +" in the result.xlsx")
        return cedOfLFP*0.2777777777
    

    ### Create outputs for a productsystem for Recepi2016
    def calcRECIPIMP2016HWithOpenLCA(self, productsystem):
        client = olca.Client(8080)
        setup = olca.CalculationSetup()
        print("running openLCA...", end="\r")
        impact_categories = lca.openlca(recepi, productsystem, port=8080)    
        result = client.calculate(setup)
        client.excel_export(result, 'result.xlsx')

        df = pd.read_excel('result.xlsx', header=1, sheet_name='Impacts')
        df = df.fillna(0)         
        
        recepiResult = np.array(df.iloc[:].Result)
        print("GWP100 of " + productsystem +" in kgCO2 eq. = %d" %recepiResult[2])

        df = 0
        client.dispose(result)

        print("Done! You can find the results of "+ productsystem + recepi +" in the result.xlsx")
        return recepiResult
    
    # calculates CED for system - is not used by default    
    def getAndCalcCED(self, productsystem):
        self.calcWithOpenLCA(productsystem, ced)
        df = pd.read_excel('result.xlsx', header=1, sheet_name='Impacts')
        df = df.fillna(0)

        cedOfLFP = df.iloc[-1,-1]
        print("CED of " + productsystem +" in MJ = %d" %cedOfLFP)
        print("!!Return value is given in kWh!!")
        return cedOfLFP*0.2777777777
    
# calculates from an empty sheet the result table in Open LCA and converts from it the battery specific CED result sheet
    def calcProdAndRecyclingCEDcsv(self):
        
        if self.name == 'FC 80 kW' or 'FC' or 'Hydrogen Tank':
            column_values = ['energy resources: non-renewable - energy content (HHV)', 
                    'energy resources: non-renewable, biomass - energy content (HHV)',
                    'energy resources: non-renewable, fossil - energy content (HHV)', 
                    'energy resources: non-renewable, nuclear - energy content (HHV)',
                    'energy resources: renewable - energy content (HHV)',
                    'energy resources: renewable, biomass - energy content (HHV)',
                    'energy resources: renewable, geothermal - energy content (HHV)',
                    'energy resources: renewable, geothermal, solar, wind - energy content (HHV)',
                    'energy resources: renewable, solar - energy content (HHV)',
                    'energy resources: renewable, water - energy content (HHV)',
                    'energy resources: renewable, wind - energy content (HHV)',
                    'total - energy content (HHV)']
            result = np.zeros((len(self.fcProdsystems),len(column_values)))
            itemn = 0
            for key in self.fcProdsystems:
                value = self.fcProdsystems[key]
                res = self.calcCEDWithOpenLCA(value,ced)
                result[itemn] = res
                itemn += 1

            index_values = list(self.fcProdsystems.values())
            
            df = pd.DataFrame(data = result, 
                            index = index_values, 
                            columns = column_values)

            filepath  = self.name + 'CED.csv'
            df.to_csv(filepath)

            # displaying the dataframe
            #print(df)


        
        else: 
            print('Error, your FC-System is not in the List')            
            return
        #else: print("sry")

    def calcProdAndRecyclingReCePi2016csv(self):
        if self.name == 'FC 80 kW' or 'FC' or 'Hydrogen Tank':
            column_values = ['acidification: terrestrial - terrestrial acidification potential (TAP)', 
                            'climate change - global warming potential (GWP100)',
                            'ecotoxicity: freshwater - freshwater ecotoxicity potential (FETP)', 
                            'ecotoxicity: marine - marine ecotoxicity potential (METP)',
                            'ecotoxicity: terrestrial - terrestrial ecotoxicity potential (TETP)',
                            'energy resources: non-renewable, fossil - fossil fuel potential (FFP)',
                            'eutrophication: freshwater - freshwater eutrophication potential (FEP)',
                            'eutrophication: marine - marine eutrophication potential (MEP)',
                            'human toxicity: carcinogenic - human toxicity potential (HTPc)',
                            'human toxicity: non-carcinogenic - human toxicity potential (HTPnc)',
                            'ionising radiation - ionising radiation potential (IRP)',
                            'land use - agricultural land occupation (LOP)',
                            'material resources: metals/minerals - surplus ore potential (SOP)',
                            'ozone depletion - ozone depletion potential (ODPinfinite)',
                            'particulate matter formation - particulate matter formation potential (PMFP)',
                            'photochemical oxidant formation: human health - photochemical oxidant formation potential: humans (HOFP)',
                            'photochemical oxidant formation: terrestrial ecosystems - photochemical oxidant formation potential: ecosystems (EOFP)',
                            'water use - water consumption potential (WCP)']
            
            result = np.zeros((len(self.fcProdsystems),len(column_values)))
            itemn = 0
            for key in self.fcProdsystems:
                value = self.fcProdsystems[key]
                res = self.calcRECIPIMP2016HWithOpenLCA(value)
                result[itemn] = res
                itemn += 1

            index_values = list(self.fcProdsystems.values())
            df = pd.DataFrame(data = result, 
                            index = index_values, 
                            columns = column_values)
            filepath  = self.name + 'ReCePi.csv'
            df.to_csv(filepath)
            return 
        else:
            print('Error, your FC-System is not in the List')            
            return

# this function returns the desired value from the csv data you already have or have created
    def calcProdAndRecyclingFROMcsv(self, methode, impactcategory):
        # indices = [0,3,4]
    # import data file
        filepath  = self.name + methode + '.csv'
        df = pd.read_csv(filepath, delimiter = ',', header= 0, index_col= 0)
    # create array to store information
        impactofCellChemistryForMethode = np.zeros((len(df.index),1))
    # fill array with data
        dflen = len(df.index)
        for i in range(dflen):
            impactofCellChemistryForMethode[i] = df.iloc[i][impactcategory]
        # return impactofCellChemistryForMethode[indices].sum()
        # multiply each element with amount of part for 1 kW fuelCell to calculate a FC of 1 kW and multiply it later
        return impactofCellChemistryForMethode.sum()
    
    # this function returns the desired value from the csv data you already have or have created
    def calcGWP100FROMcsv(self, methode, impactcategory, index):
        indices = index
    # import data file
        filepath  = self.name + methode + '.csv'
        df = pd.read_csv(filepath, delimiter = ',', header= 0, index_col= 0)
    # create array to store information
        impactofCellChemistryForMethode = np.zeros((len(df.index),1))
    # fill array with data
        dflen = len(df.index)
        for i in range(dflen):
            impactofCellChemistryForMethode[i] = df.iloc[i][impactcategory]
        return impactofCellChemistryForMethode[indices].sum()



class FuelCellStack(FuelCell):
    def __init__(self,typeFC = 'FC 80 kW' or 'FC', power = 0):
        super().__init__(typeFC)
        self.power    = power
        if self.power < 75:
            self.weight = 72
        elif 75 < self.power <= 75:
            self.weight = 80
        elif 75 < self.power <= 150:
            self.weight = 140
        elif 150 < self.power == 300:
            self.weight = 280
        else:
            print('Your FC System is not in the List (40, 75, 150, 300)')
        self.totalCED = self.power * self.calcProdAndRecyclingFROMcsv('CED', 'total - energy content (HHV)')
        self.totalGWP100 = self.power * self.calcProdAndRecyclingFROMcsv('ReCePi', 'climate change - global warming potential (GWP100)')
        
        self.prodGWP100 = self.power * self.calcGWP100FROMcsv('ReCePi', 'climate change - global warming potential (GWP100)',[0])
        self.recyclingHydroGWP100 = self.power * self.calcGWP100FROMcsv('ReCePi', 'climate change - global warming potential (GWP100)',[1,2,3,4,5,6,7,8,9,10,11,12,13,14])



class HydrogenTankSystem(FuelCell):
    def __init__(self,tank = 'Hydrogen Tank', kgHydrogen = 0):
        super().__init__(tank)
        self.kgHydrogen = kgHydrogen
        self.emptyweight = 101.2
        self.h2mass = 5
        self.h2tankCount = self.kgHydrogen//self.h2mass                                                                             # calc n tanks 
        print(self.h2tankCount)
        self.weight = self.h2tankCount * self.emptyweight + self.kgHydrogen

        self.prodGWP100 = self.h2tankCount * self.calcGWP100FROMcsv('ReCePi', 'climate change - global warming potential (GWP100)',[0])
        self.recyclingHydroGWP100 = self.h2tankCount * self.calcGWP100FROMcsv('ReCePi', 'climate change - global warming potential (GWP100)',[1])

        self.totalCED = self.h2tankCount*self.calcProdAndRecyclingFROMcsv('CED', 'total - energy content (HHV)')
        self.totalGWP100 = self.h2tankCount*self.calcProdAndRecyclingFROMcsv('ReCePi', 'climate change - global warming potential (GWP100)')



##### Test Tank:
# testTank = HydrogenTankSystem('Hydrogen Tank',40)
# print('Tank Prod',testTank.prodGWP100)
# print('Tank Rec',testTank.recyclingHydroGWP100)
# print('Tank Tot',testTank.totalGWP100)

# testFC = FuelCellStack("FC", 70)
# print('FC Prod',testFC.prodGWP100)
# print('FC Rec',testFC.recyclingHydroGWP100)
# print('FC Total GWP',testFC.totalGWP100)