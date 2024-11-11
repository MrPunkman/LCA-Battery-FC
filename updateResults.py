from timeit import default_timer as timer
from openlca_automation.tool import lca
import gradio as gr
import olca
import pandas as pd
import numpy as np
import datetime

client = olca.Client(8081)

# def choseCellChemistry
# Hier kann man in einem Dropdown die Zellchemien inkl. 

def calculateImpactNMC111(productSystem, impactMethod):
    setup = olca.CalculationSetup()
    now = datetime.datetime.now()
    q_start = timer()
    cell_chemistry = productSystem
    # impactMethod = 'ReCiPe 2016 Midpoint (H)'
    # q_start2 = timer()
    print("running openLCA...", end="\r")
    impact_categories = lca.openlca(impactMethod, cell_chemistry, port=8081)
    CO2_Impact = impact_categories[5].value # GWP---------------------------- spalte herausfinden für die ReCiPe 2016 Midpoint (H) und Wo China enthalten ist
    q_end = timer()
    q_duration = q_end - q_start
    print("Impact", CO2_Impact,"It took", q_duration)
    
    result = client.calculate(setup)
    client.excel_export(result, '{TS}_{PS}_{IM}.xlsx'.format(PS = productSystem, IM = impactMethod, TS = now.strftime("%Y-%m-%d %H:%M:%S")))
    return CO2_Impact

def calculateCapacity(cell_capacity):
    impact = calculateImpactNMC111() * cell_capacity
    print("The GWP100 Impact of a ", cell_capacity, "kWh', 'Li-Ion Battery is", impact, "kg CO2 eq.")
    return "The GWP100 Impact of a ", cell_capacity



# impact methods: 'ReCiPe 2016 Midpoint (H)'
# productsystems