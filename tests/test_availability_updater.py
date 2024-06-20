import unittest
from unittest.mock import patch, MagicMock

import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
external_directory = os.path.join(current_dir, "..")
sys.path.append(external_directory)

from controllers.AvailabilityUpdater import (
    generate_available_times_per_day,
    process_class_schedule,
    condense_available_times_per_day,
    format_ranges_12_hour,
    getAvailableRanges,
    updateAvailabilityForEmployees,
)


class TestAvailabilityUpdater(unittest.TestCase):

    @patch("AvailabilityUpdater.updateAvailability")
    def test_update_availability(self, mock_update_availability):
        employee_id_list = [123456789]
        updateAvailabilityForEmployees(employee_id_list)
        mock_update_availability.assert_called()

    def test_generate_available_times_per_day(self):
        available_times_per_day = generate_available_times_per_day()
        self.assertEqual(len(available_times_per_day), 7)
        self.assertEqual(len(available_times_per_day["Monday"]), 24 * 12)

    def test_process_class_schedule(self):
        available_times_per_day = generate_available_times_per_day()
        class_schedule = [
            {
                "subject": "Physics",
                "start": "09:00:00 AM",
                "end": "11:00:00 AM",
                "meetingDays": "MWF",
            }
        ]
        updated_times = process_class_schedule(available_times_per_day, class_schedule)
        self.assertNotEqual(updated_times["Monday"], available_times_per_day["Monday"])

    def test_condense_available_times_per_day(self):
        available_times_per_day = generate_available_times_per_day()
        condensed_times = condense_available_times_per_day(available_times_per_day)
        self.assertIsInstance(condensed_times["Monday"], list)

    def test_format_ranges_12_hour(self):
        ranges = ["09:00-11:00", "13:00-15:00"]
        formatted_ranges = format_ranges_12_hour(ranges)
        self.assertEqual(formatted_ranges, "09:00am-11:00am;01:00pm-03:00pm;")

    @patch("AvailabilityUpdater.getStudentSchedule")
    def test_getAvailableRanges(self, mock_getStudentSchedule):
        mock_getStudentSchedule.return_value = [
            {
                "subject": "Physics",
                "start": "09:00:00 AM",
                "end": "11:00:00 AM",
                "meetingDays": "MWF",
            }
        ]
        employee_id = 123456789
        ranges = getAvailableRanges(employee_id)
        self.assertIsInstance(ranges, list)


if __name__ == "__main__":
    unittest.main()
