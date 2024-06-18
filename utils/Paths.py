from enum import Enum

class Paths(Enum):
    SS_SCHEDULE_SHIFTS = "/2023.1/api/io/ScheduleShift"
    SS_SCHEDULE = f"/2023.1/api/io/Schedule"
    SS_LOCATIONS = f"/2023.1/api/io/Business"
    SS_AVAILABILITY = f"/2023.1/api/io/GlobalAvailDay/json"
    SS_EMPLOYEES = f"/2023.1/api/io/Employee/tab"
    SS_EMPLOYEES_LOCATION = f"/2023.1/api/io/LocalEmployee/tab"

    
    