from ade_enseirb import Planning, Event

import unittest
import datetime


def create_empty_planning():
    return Planning()


def create_one_event_planning(start, end, summary, location):
    planning = Planning()
    planning._add_event(start, end, summary, location)
    return planning


def create_planning_with_list(events):
    planning = Planning()
    for start, end, summary, location in events:
        planning._add_event(start, end, summary, location)
    return planning


class TestPlanning(unittest.TestCase):

    def test_empty_planning(self):
        planning = Planning()

        self.assertEqual(planning.event_count(), 0)
        self.assertEqual(planning.events_done(), 0)
        self.assertIsNone(planning.event_running())

        self.assertEqual(planning.day_duration(), datetime.timedelta(0))
        self.assertEqual(planning.work_duration(), datetime.timedelta(0))

        self.assertRaises(ValueError, planning.first_event)
        self.assertRaises(ValueError, planning.start_of_first_event)
        self.assertRaises(ValueError, planning.last_event)
        self.assertRaises(ValueError, planning.end_of_last_event)

    def test_one_past_event_planning(self):
        planning = create_one_event_planning(
            datetime.datetime(2023, 1, 1, 8, 0),
            datetime.datetime(2023, 1, 1, 10, 0),
            'Event',
            'Location'
        )

        self.assertEqual(planning.event_count(), 1)
        self.assertEqual(planning.events_done(), 1)
        self.assertIsNone(planning.event_running())

        self.assertEqual(planning.day_duration(), datetime.timedelta(hours=2))
        self.assertEqual(planning.work_duration(), datetime.timedelta(hours=2))

        self.assertEqual(planning.start_of_first_event(), datetime.datetime(2023, 1, 1, 8, 0))
        self.assertEqual(planning.end_of_last_event(), datetime.datetime(2023, 1, 1, 10, 0))

    def test_one_future_event_planning(self):
        planning = create_one_event_planning(
            datetime.datetime(3000, 1, 1, 8, 0),
            datetime.datetime(3000, 1, 1, 10, 0),
            'Event',
            'Location'
        )

        self.assertEqual(planning.event_count(), 1)
        self.assertEqual(planning.events_done(), 0)
        self.assertIsNone(planning.event_running())

        self.assertEqual(planning.day_duration(), datetime.timedelta(hours=2))
        self.assertEqual(planning.work_duration(), datetime.timedelta(hours=2))

        self.assertEqual(planning.start_of_first_event(), datetime.datetime(3000, 1, 1, 8, 0))
        self.assertEqual(planning.end_of_last_event(), datetime.datetime(3000, 1, 1, 10, 0))

    def test_long_planning(self):
        planning = create_planning_with_list([
            [datetime.datetime(2023, 1, 1, 8, 0), datetime.datetime(2023, 1, 1, 10, 0), 'Event 1', 'Location 1'],
            [datetime.datetime(2023, 1, 1, 10, 0), datetime.datetime(2023, 1, 1, 12, 0), 'Event 2', 'Location 2'],
            [datetime.datetime(2023, 1, 1, 12, 0), datetime.datetime(3000, 1, 1, 14, 0), 'Event 3', 'Location 3'],
            [datetime.datetime(3000, 1, 1, 14, 0), datetime.datetime(3000, 1, 1, 16, 0), 'Event 4', 'Location 4'],
            [datetime.datetime(3000, 1, 1, 16, 0), datetime.datetime(3000, 1, 1, 18, 0), 'Event 5', 'Location 5']])

        self.assertEqual(planning.event_count(), 5)
        self.assertEqual(planning.events_done(), 2)

        event_running = planning.event_running()

        self.assertIsNotNone(event_running)
        self.assertEqual(event_running.start, datetime.datetime(2023, 1, 1, 12, 0))
        self.assertEqual(event_running.end, datetime.datetime(3000, 1, 1, 14, 0))

        self.assertEqual(planning.start_of_first_event(), datetime.datetime(2023, 1, 1, 8, 0))
        self.assertEqual(planning.end_of_last_event(), datetime.datetime(3000, 1, 1, 18, 0))


if __name__ == '__main__':
    unittest.main()
