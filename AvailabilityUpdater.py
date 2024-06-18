##################################################### Update Availability ##############################################
from datetime import datetime, timedelta

from api_calls.schedule_source_api.schedule_source_api import updateAvailability, getAllActiveEmployees, getEmployeesAtLocation
from api_calls.workday_api.workday_api import getStudentSchedule

#Generate a dictionary with available times for each day of the week.
def generate_available_times_per_day():
    available_times_per_day = {day: [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in range(0, 60, 5)] for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]}
    return available_times_per_day

#Convert a time string in "HH:MM" format to minutes from midnight.
def time_to_minutes(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

#Remove times from the available times list that fall within the class time range.
def remove_class_times(available_times, start, end):
    return [time for time in available_times if not (start <= time_to_minutes(time) < end)]

#Process the class schedule and update available times by removing class times.
def process_class_schedule(available_times_per_day, class_schedule):
    days_map = {'U': 'Sunday', 'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday', 'A': 'Saturday'}

    for class_info in class_schedule:
        start_time_minutes = time_to_minutes(datetime.strptime(class_info["start"], "%I:%M:%S %p").strftime("%H:%M"))
        end_time_minutes = time_to_minutes(datetime.strptime(class_info["end"], "%I:%M:%S %p").strftime("%H:%M"))
        meeting_days = class_info["meetingDays"]

        for day in meeting_days:
            day_name = days_map[day]
            available_times_per_day[day_name] = remove_class_times(available_times_per_day[day_name], start_time_minutes, end_time_minutes)

    return available_times_per_day

#Condense a list of times into ranges.
def condense_times(times):
    if not times:
        return []

    ranges = []
    start = previous = times[0]

    for time in times[1:]:
        if time_to_minutes(time) != time_to_minutes(previous) + 5:
            ranges.append(f"{start}-{previous}")
            start = time
        previous = time

    ranges.append(f"{start}-{previous}")
    return ranges

# Condense the available times into ranges for each day of the week
def condense_available_times_per_day(available_times_per_day):
    return {day: condense_times(times) for day, times in available_times_per_day.items()}

#Convert a time string from 24-hour format to 12-hour format.
def convert_to_12_hour_format(time_str):
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M%p").lstrip('0').lower()

#Convert and format time ranges from 24-hour format to 12-hour format.
def format_ranges_12_hour(ranges):
    formatted_ranges = []
    for time_range in ranges:
        start, end = time_range.split('-')
        start_12 = convert_to_12_hour_format(start)
        end_12 = convert_to_12_hour_format(end)
        formatted_ranges.append(f"{start_12}-{end_12}")
    return ';'.join(formatted_ranges) + ';'

#Get the available time ranges for a given employee using their class schedule
def getAvailableRanges(employee_id):
    employee_classSchedule = getStudentSchedule(employee_id)
    
    # Generate available times per day
    available_times_per_day = generate_available_times_per_day()
    # Process the class schedule to update available times
    available_times_per_day = process_class_schedule(available_times_per_day, employee_classSchedule)
    # Condense available times into ranges for each day
    condensed_available_times_per_day = condense_available_times_per_day(available_times_per_day)

    avail_ranges = []
    # Convert to 12-hour format and print the results
    for day, ranges in condensed_available_times_per_day.items():
        formatted_ranges = format_ranges_12_hour(ranges)
        avail_ranges.append(formatted_ranges)
        
    return avail_ranges

# Uses the ss api client to update the availability on schedule source's remote server for a given location
def updateAvailabilityForEmployees(employee_id_list):
    for employee_id in employee_id_list:
        ranges = getAvailableRanges(employee_id)
        updatedData = []
        for i in range(1, 8):
            updatedData.append({
                "DayId": i,
                "AvailableRanges": ranges[i-1], 
                "EmployeeExternalId": employee_id,
                "Enabled": 1,
                "Rank": 1
            })
        updateAvailability(updatedData)
        print("UPDATED: " + str(employee_id))