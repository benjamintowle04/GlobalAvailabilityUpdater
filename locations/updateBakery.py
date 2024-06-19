import sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "..")
sys.path.append(external_directory)

from controllers.AvailabilityUpdater import updateAvailabilityForEmployees
from api_calls.schedule_source_api.schedule_source_api import getEmployeesAtLocation

def updateBakery():
    employee_id_list = getEmployeesAtLocation("Bakery")
    updateAvailabilityForEmployees(employee_id_list)
    print("FINISHED UPDATING AVAILABILITY FOR Bakery")

