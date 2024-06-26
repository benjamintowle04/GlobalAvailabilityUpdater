# Global Availability Updater

The Global Availability Updater is a Python script designed to streamline scheduling management for the Dining Student Staffing Office at Iowa State University. It automates the process of updating student availability, ensuring efficient coordination of schedules and minimizing conflicts across the university's dining facilities. The script runs through all dining locations and updates every employee's availability for each dining facility. Each employee's availability is determined by their respective class schedule retrieved from workday's external api system. The data recieved from workday's class schedules are streamlined into the availability of each employee in schedule source. As a result, users who look to see who is available to take a shift from a schedule template will see who can and cannot work that shift based on their classes. 



## Overview

Managing student schedules and work shifts in dining halls can be complex and time-consuming. The Global Availability Updater simplifies this process by automating the retrieval and updating of student availability data. It integrates seamlessly with Iowa State's Workday API to gather student schedules and cross-references this information with available shifts from the Schedule Source API. This ensures that scheduling conflicts are able to be viewed in Schedule Source.



## Description

The Global Availability Updater operates in a straightforward manner:

1. **Data Retrieval**: It retrieves student schedules from Iowa State's Workday API, capturing essential information such as class schedules and commitments.

2. **Availability Update**: Using the obtained data, the updater updates student availability in the Schedule Source API. It ensures that class times are excluded from potential work shifts, minimizing conflicts.

3. **Real-time Updates**: The script executes automatic daily updates to maintain the accuracy of availability data, promptly reflecting any modifications to student schedules. This ensures that the Schedule Source availability is always up-to-date.

4. **Error Handling**: Robust error handling mechanisms are in place to address unforeseen challenges, ensuring smooth operation and reliability.



![diagram-export-18-06-2024-10_41_20](https://github.com/benjamintowle04/GlobalAvailabilityUpdater/assets/170199259/dede0de1-61a4-4560-bc96-ce1ff0851a56)

