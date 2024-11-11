''' Run this file to create the data for further investigations. It is a time saving methode to not run OpenLCA '''

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


cellNMC811 = CellChemistry("NMC811")
cellNMC811.calcProdAndRecyclingCEDcsv()
cellNMC811.calcProdAndRecyclingReCePi2016csv()


# cellNMC111= CellChemistry("NMC111")
# cellNMC111.calcProdAndRecyclingCEDcsv()
# cellNMC111.calcProdAndRecyclingReCePi2016csv()

# cellNCA= CellChemistry("NCA")
# cellNCA.calcProdAndRecyclingCEDcsv()
# cellNCA.calcProdAndRecyclingReCePi2016csv()

# cellLFP= CellChemistry('LFP')
# cellLFP.calcProdAndRecyclingCEDcsv()
# cellLFP.calcProdAndRecyclingReCePi2016csv()

# fuelCell= FuelCell('FC')
# fuelCell.calcProdAndRecyclingCEDcsv()
# fuelCell.calcProdAndRecyclingReCePi2016csv()

tank = FuelCell('Hydrogen Tank' )
tank.calcProdAndRecyclingCEDcsv()
tank.calcProdAndRecyclingReCePi2016csv()












