#File in charge of scheduling each location to update their availability on schedule source's remote server.
from locations.updateBakery import updateBakery
from locations.updateCafes import updateCafes
from locations.updateConvos import updateConvos 
from locations.updateClydes import updateClydes
from locations.updateFoodStores import updateFoodStores
from locations.updateFriley import updateFriley
from locations.updateHawthorn import updateHawthorn
from locations.updateMUFC import updateMUFC 
from locations.updateMUMKT import updateMUMKT
from locations.updatePlato import updatePlato
from locations.updateSeasons import updateSeasons
from locations.updateSummer import updateSummer
from locations.updateWSM import updateWSM
from locations.updateUDM import updateUDM

def main():
    updateBakery()
    # updateCafes()
    # updateClydes()
    # updatePlato()
    # updateUDM()
    # updateConvos()
    # updateHawthorn()
    # updateWSM()
    # updateSummer()
    # updateSeasons()
    # updateMUMKT()
    # updateMUFC()
    # updateFriley()
    # updateFoodStores()
    print("FINISHED UPDATING AVAILABILITY FOR ALL LOCATIONS")
    
if __name__ == "__main__":
    main()