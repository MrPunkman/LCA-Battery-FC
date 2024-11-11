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
# and subclasses to build a vehicle drivetrain


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
from batteryDef import *

class CellChemistry:
#set Chemistry to NMC811, NMC111, NCA, LFP, FC
# in case, you don't have the .csv data, create new batteries/cellchemistries and run the following lines depending on the system you need the csv data
    # cellNMC811.calcProdAndRecyclingCEDcsv()   
    #def __init__(self, chemistry = 'NMC811' or 'NMC111' or 'LFP' or 'NCA'):

    #cellNMC811.calcProdAndRecyclingReCePi2016csv()
    # cellNMC111.calcProdAndRecyclingCEDcsv()                  # 
    #cellNMC111.calcProdAndRecyclingReCePi2016csv()
    # cellNCA.calcProdAndRecyclingCEDcsv()                     # 
    #cellNCA.calcProdAndRecyclingReCePi2016csv()
    # cellLFP.calcProdAndRecyclingCEDcsv()                     # 
    #cellLFP.calcProdAndRecyclingReCePi2016csv()
    # kWFuelcell.calcProdAndRecyclingCEDcsv()                  # 
    #kWFuelcell.calcProdAndRecyclingReCePi2016csv()
    # fuelCell.calcProdAndRecyclingCEDcsv()                    # 
    #fuelCell.calcProdAndRecyclingReCePi2016csv()

# impact cathegories CED:
        # "energy resources: non-renewable, biomass - energy content (HHV)"
        # "energy resources: non-renewable, fossil - energy content (HHV)"
        # "energy resources: non-renewable, nuclear - energy content (HHV)" "energy resources: renewable - energy content (HHV)"
        # "energy resources: renewable, biomass - energy content (HHV)"
        # "energy resources: renewable, geothermal - energy content (HHV)"
        # "energy resources: renewable, geothermal, solar, wind - energy content (HHV)"
        # "energy resources: renewable, solar - energy content (HHV)"
        # "energy resources: renewable, water - energy content (HHV)"
        # "energy resources: renewable, wind - energy content (HHV)"
        # 'total - energy content (HHV)'

 # impact cathegories ReCePi:
 # acidification: terrestrial - terrestrial acidification potential (TAP)
 # climate change - global warming potential (GWP100)
 # ecotoxicity: freshwater - freshwater ecotoxicity potential (FETP)
 # ecotoxicity: marine - marine ecotoxicity potential (METP)
 # ecotoxicity: terrestrial - terrestrial ecotoxicity potential (TETP)
 # "energy resources: non-renewable, fossil - fossil fuel potential (FFP)"
 # eutrophication: freshwater - freshwater eutrophication potential (FEP)
 # eutrophication: marine - marine eutrophication potential (MEP)
 # human toxicity: carcinogenic - human toxicity potential (HTPc)
 # human toxicity: non-carcinogenic - human toxicity potential (HTPnc)
 # ionising radiation - ionising radiation potential (IRP)
 # land use - agricultural land occupation (LOP)
 # material resources: metals/minerals - surplus ore potential (SOP)
 # ozone depletion - ozone depletion potential (ODPinfinite)
 # particulate matter formation - particulate matter formation potential (PMFP)
 # photochemical oxidant formation: human health - photochemical oxidant formation potential: humans (HOFP)
 # photochemical oxidant formation: terrestrial ecosystems - photochemical oxidant formation potential: ecosystems (EOFP)
 # water use - water consumption potential (WCP)       

        # Einheiten könnte man ergänzen
    def __init__(self, chemistry = 'NMC811' or 'NMC111' or 'LFP' or 'NCA'):
        self.name              = chemistry          # give a name to the cell chemistry for later plots
        self.chemistry         = chemistry          # used for later calculations. Same as name but different usage
                                                    # Battery system an attributes
        if self.chemistry == 'NMC811':
            self.chemistry = prodNMC811
            self.batterycollectionAndSorting = batterycollectionAndTransport
            self.recyclingHydro = NMC811Hydrometallurgy
            self.recyclingPyro = NMC811Pyrometallurgy
            self.energyDensity = 149

        elif self.chemistry == 'NMC111':
            self.chemistry = prodNMC111
            self.batterycollectionAndSorting = batterycollectionAndTransport
            self.recyclingHydro = NMC111Hydrometallurgy
            self.recyclingPyro = NMC111Pyrometallurgy
            self.energyDensity = 143

        elif self.chemistry == 'LFP':
            self.chemistry = prodLFP
            self.batterycollectionAndSorting = batterycollectionAndTransport
            self.recyclingHydro = LFPHydrometallurgy
            self.recyclingPyro = LFPPyrometallurgy
            self.energyDensity = 116

        elif self.chemistry == 'NCA':
            self.chemistry = prodNCA
            self.batterycollectionAndSorting = batterycollectionAndTransport
            self.recyclingHydro = NCAHydrometallurgy
            self.recyclingPyro = NCAPyrometallurgy
            self.energyDensity = 158
        
        else: print('Your System is not in the list')


    ### Create outputs for a productsystem for Impact methode

    def calcCEDWithOpenLCA(self, productsystem, impactMethod):
        client = olca.Client(8080)
        setup = olca.CalculationSetup()
        print("running openLCA...", end="\r")
        impact_categories = lca.openlca(impactMethod, productsystem, port=8080)    
        result = client.calculate(setup)
        client.excel_export(result, 'result.xlsx')

        df = pd.read_excel('result.xlsx', header=1, sheet_name='Impacts')
        df = df.fillna(0)

        cedOfLFP = np.array(df.iloc[:].Result)
        print("CED of " + productsystem +" in MJ = %d" %cedOfLFP[11])
        print("!!Return value is given in kWh!!")

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
        if self.chemistry == FC80kW:
            self.production = self.calcCEDWithOpenLCA(self.chemistry, ced)
            recyclingHydromet = self.calcCEDWithOpenLCA(self.recyclingHydro,ced)
            return np.array((self.production, recyclingHydromet))
        
        else: 
            # self.chemistry == prodNMC811 batteryDismantling
            production = self.calcCEDWithOpenLCA(self.chemistry, ced)
            batColAndSorti = self.calcCEDWithOpenLCA(self.batterycollectionAndSorting, ced)
            
            
            recyclingPyromet = self.calcCEDWithOpenLCA(self.recyclingPyro, ced)
            recyclingHydromet = self.calcCEDWithOpenLCA(self.recyclingHydro, ced)

            array = np.array((production, batColAndSorti, recyclingPyromet, recyclingHydromet))
            # array = np.array([resultCED, resultgwp100, resulthtpc, resultSOP])

            # creating a list of index names
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

            # creating a list of column names
            index_values = ['Production', 'CollectionAndSorting', 'Recycling Pyrometallurgy', 'Recycling Hydrometallurgy']

            # creating the dataframe
            df = pd.DataFrame(data = array, 
                            index = index_values, 
                            columns = column_values)

            filepath  = self.name + 'CED.csv'
            df.to_csv(filepath)

            # displaying the dataframe
            print(df)
            
            return np.array((production, batColAndSorti, recyclingPyromet, recyclingHydromet))
        #else: print("sry")
                                                                                                # create recepi 2016 midpoint h csv data
    def calcProdAndRecyclingReCePi2016csv(self):
        
        if self.chemistry == FC80kW:
            self.production = self.calcCEDWithOpenLCA(self.chemistry, recepi)
            recyclingHydromet = self.calcCEDWithOpenLCA(self.recyclingHydro,recepi)
            return np.array((self.production, recyclingHydromet))
        
        else:
            production = self.calcRECIPIMP2016HWithOpenLCA(self.chemistry)
            batColAndSorti = self.calcRECIPIMP2016HWithOpenLCA(self.batterycollectionAndSorting)
            recyclingPyromet = self.calcRECIPIMP2016HWithOpenLCA(self.recyclingPyro)
            recyclingHydromet = self.calcRECIPIMP2016HWithOpenLCA(self.recyclingHydro)


            array = np.array((production, batColAndSorti, recyclingPyromet, recyclingHydromet))
            # creating a list of column names
            index_values = ['Production', 'CollectionAndSorting', 'Recycling Pyrometallurgy', 'Recycling Hydrometallurgy']

            # creating a list of index names
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
            # creating the dataframe
            df = pd.DataFrame(data = array, 
                            index = index_values, 
                            columns = column_values)

            filepath  = self.name + 'ReCePi.csv'
            df.to_csv(filepath)

            # displaying the dataframe
            print(df)

            return df


# this function returns the desired value from the csv data you already have or have created
    def calcProdAndRecyclingFROMcsv(self, methode, impactcategory):
        indices = [0,1,2]
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

        

# ---------------------------------------------------------------------------------------------------------
# class to create a battery

class Batterie(CellChemistry):
    def __init__(self, cellchemistry = 'NMC811' or 'NMC111' or 'LFP' or 'NCA', capacity = 1):
        super().__init__(cellchemistry)
        self.capacity   = capacity
    # weight in kg !
        if self.capacity < 1000:                                                # if capacity is given in kWh calculate in Wh
            self.weightofBattery = (self.capacity*1000)/self.energyDensity
        else:                                                                   # else calculate in Wh
            self.weightofBattery = (self.capacity) /self.energyDensity


        self.prodGWP100 = self.weightofBattery*self.calcGWP100FROMcsv('ReCePi', 'climate change - global warming potential (GWP100)',[0])
        self.recyclingHydroGWP100 = self.weightofBattery*self.calcGWP100FROMcsv('ReCePi', 'climate change - global warming potential (GWP100)',[2,3])

        self.totalCED = self.weightofBattery*self.calcProdAndRecyclingFROMcsv('CED', 'total - energy content (HHV)')
        self.totalGWP100 = self.weightofBattery*self.calcProdAndRecyclingFROMcsv('ReCePi', 'climate change - global warming potential (GWP100)')

##### Test Battery:
# test = Batterie('NMC811',100)
# print(test.prodGWP100)
# print(test.recyclingHydroGWP100)
# print(test.totalCED)