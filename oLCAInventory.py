# this file contains the classes for the vehicles 
# and subclasses too build a vehicle drivetrain


# allowed abrevations for cell chemistries
        # 'NMC811'
        # 'NMC111'
        # 'LFP'
        # 'NCA'
        # 'FC'    ---->>>> contains all processes for the productioin of a pack
        # 'FC 80 kW'


# productions:

prodNMC811  = 'battery production, Li-ion, NMC811, rechargeable, prismatic | battery, Li-ion, NMC811, rechargeable, prismatic | Consequential, U - China 2021'
prodNMC111  = 'battery production, Li-ion, NMC111, rechargeable, prismatic | battery, Li-ion, NMC111, rechargeable, prismatic | Consequential, U - China 2021'
prodLFP     = 'battery production, Li-ion, LFP, rechargeable, prismatic | battery, Li-ion, LFP, rechargeable, prismatic | Consequential, U - China 2021'
prodNCA     = 'battery production, Li-ion, NCA, rechargeable, prismatic | battery, Li-ion, NCA, rechargeable, prismatic | Consequential, U - China 2021'
FC80kW      = 'FC 80 kW'
FC          = 'FC'


# recycling
batterycollectionAndTransport = 'Li-Ion Battery Recycling, GREET, Collection and Transportation - EverBatt'

LFPbatteryDisassembly = 'Li-Ion Battery Recycling, GREET, LFP Disassembly - EverBatt'
#batteryShredding = 'Li-Ion Battery Recycling, shredding and sorting'
LFPHydrometallurgy = 'Li-Ion Battery Recycling, GREET, LFP Hydrometallurgical - EverBatt'
LFPPyrometallurgy = 'Li-Ion Battery Recycling, GREET, LFP Pyrometallurgical - EverBatt'

NCAbatteryDisassembly = 'Li-Ion Battery Recycling, GREET, LFP Disassembly - EverBatt'
NCAHydrometallurgy = 'Li-Ion Battery Recycling, GREET, NCA Hydrometallurgical - EverBatt'
NCAPyrometallurgy =  'Li-Ion Battery Recycling, GREET, NCA Pyrometallurgical - EverBatt'

NMC111batteryDisassembly = 'Li-Ion Battery Recycling, GREET, NMC111 Disassembly - EverBatt'
NMC111Hydrometallurgy = 'Li-Ion Battery Recycling, GREET, NMC111, Hydrometallurgical - EverBatt'
NMC111Pyrometallurgy = 'Li-Ion Battery Recycling, GREET, NMC111, Pyrometallurgical - EverBatt'

NMC811batteryDisassembly = 'Li-Ion Battery Recycling, GREET, NMC811 Disassembly - EverBatt'
NMC811Hydrometallurgy = 'Li-Ion Battery Recycling, GREET, NMC811, Hydrometallurgical - EverBatt'
NMC811Pyrometallurgy =  'Li-Ion Battery Recycling, GREET, NMC811, Pyrometallurgical - EverBatt'

# FC recycling:


# impact methods
ced = 'ecoinvent - Cumulative Energy Demand (CED)'
recepi = 'ecoinvent - ReCiPe 2016 v1.03, midpoint (H)'


# impact categories:
gwp100 = 'climate change - global warming potential (GWP100)'
htpc = 'human toxicity: carcinogenic - human toxicity potential (HTPc)'
sop = 'material resources: metals/minerals - surplus ore potential (SOP)'


