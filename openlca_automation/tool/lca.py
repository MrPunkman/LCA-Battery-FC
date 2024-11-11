import olca

def openlca(impactMethod, productsystem_name: str, port: int = 8080):
    """
    This function takes the energy source specific parameters from ecoinvent database and calculates the environmental impact using OpenLCA

    Arguments:
        impactMethod: name of the product method (copy name from OpenLCA)
        productsystem_name: name of product system (copy name from OpenLCA)
        port: port for IPC connection (has to be initialized in OpenLCA: Tools->Developer-Tools->IPC Server
                (optional, default: 8080) - if the port is not found in the first calculation, try to run the calculation once more and it sould work
    Return:
        openlca_result.impact_results: LCA impact results from OpenLCA (array of the impact categories of CML 2001 (superseded))
    """

    # setting up IPC connection (port may have to be adjusted)
    client = olca.Client(port)

    # get product system references
    productsystem = client.find(olca.ProductSystem, productsystem_name)

    # initialize calculation setup
    setup = olca.CalculationSetup()

    # set calculation type (http://greendelta.github.io/olca-schema/CalculationType.html)
    setup.calculation_type = olca.CalculationType.CONTRIBUTION_ANALYSIS	

    # set impact method
    setup.impact_method = client.find(olca.ImpactMethod, impactMethod) 

    # set reference product system for energy production
    setup.product_system = productsystem
    # run calculation
    openlca_result = client.calculate(setup)

    if openlca_result.impact_results is None:
        print('Currently you are out of RAM Memory or the chosen product system/impact method could not be found. Please close some other programs to repeat the calculation.')

    client.excel_export(openlca_result, 'result.xlsx')
    return openlca_result.impact_results 

 