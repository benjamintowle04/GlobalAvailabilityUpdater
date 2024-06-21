import unittest
from unittest.mock import patch, MagicMock

import controllers.availabilityUpdater

from controllers.availabilityUpdater import (
    generate_available_times_per_day,
    process_class_schedule,
    condense_available_times_per_day,
    format_ranges_12_hour,
    getAvailableRanges,
    updateAvailabilityForEmployees,
)

print("Hello World")

class TestAvailabilityUpdater(unittest.TestCase):

    @patch("controllers.availabilityUpdater.getAvailableRanges")
    def test_getAvailableRanges(self, mock_getAvailableRanges):
        print("Testing")
        mock_schedules = []

        #TESTING A NORMAL SCHEDULE FOR BASIC FUNCTIONALITY
        mock_schedules.append([
            {
                "subject": "Physics",
                "start": "08:00:00 AM",
                "end": "9:00:00 AM",
                "meetingDays": "MWF",
            }
        ])

        #TEST A FULL SCHEDULE
        mock_schedules.append([
            {
                "subject": "Physics",
                "start": "12:00:00 AM",
                "end": "11:59:00 PM",
                "meetingDays": "UMTWRFS",
            }
        ])

        #TEST AN EMPTY SCHEDULE
        mock_schedules.append([])


        #TEST AN OVERLAPPING SCHEDULE
        mock_schedules.append([
            {
                "subject": "Physics",
                "start": "12:00:00 PM",
                "end": "1:00:00 PM",
                "meetingDays": "MWF",
            },
            {
                "subject": "Physics",
                "start": "11:00:00 AM",
                "end": "1:00:00 PM",
                "meetingDays": "MWF",
            }

        ])

        test_cases = [
            {
                "schedule": mock_schedules[0],
                "expected_return": [
                    '12:00am-11:55pm;', 
                    '12:00am-7:55am;9:00am-11:55pm;', 
                    '12:00am-11:55pm;', 
                    '12:00am-7:55am;9:00am-11:55pm;', 
                    '12:00am-11:55pm;', 
                    '12:00am-7:55am;9:00am-11:55pm;', 
                    '12:00am-11:55pm;'
                ]
            },
            {
                "schedule": mock_schedules[1],
                "expected_return": [
                    ';',
                    ';',
                    ';',
                    ';',
                    ';',
                    ';',
                    ';'
                ]
            },
            {
                "schedule": mock_schedules[2],
                "expected_return": [
                    '12:00am-11:55pm;',
                    '12:00am-11:55pm;',
                    '12:00am-11:55pm;',
                    '12:00am-11:55pm;',
                    '12:00am-11:55pm;',
                    '12:00am-11:55pm;',
                    '12:00am-11:55pm;'
                ]
            },
            {
                "schedule": mock_schedules[3],
                "expected_return": [
                    '12:00am-11:55pm;',
                    '12:00am-10:55am;1:00pm-11:55pm;',
                    '12:00am-11:55pm;',
                    '12:00am-10:55am;1:00pm-11:55pm;'
                    '12:00am-11:55pm;',
                    '12:00am-10:55am;1:00pm-11:55pm;',
                    '12:00am-11:55pm;'
                ]
            }

            # Add more test cases as needed
        ]

        i = 0
        for case in test_cases:
            with self.subTest():
                ranges = getAvailableRanges(0, case["schedule"])
                self.assertIsInstance(ranges, list)
                self.assertListEqual(ranges, case["expected_return"])
            i += 1


if __name__ == "__main__":
    unittest.main()
