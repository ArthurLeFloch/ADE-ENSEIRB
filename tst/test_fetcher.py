from ade_enseirb.cas import CASClient
from ade_enseirb.ade_fetcher import ADEFetcher

import unittest
import datetime
from getpass import getpass

cas_client = CASClient(input('Username: '), getpass())
cas_client.login()

ade_fetcher = ADEFetcher(cas_client.get_session())
ade_fetcher.connect()
ade_fetcher.load_data()


class TestFetcher(unittest.TestCase):

    def test_get_student_id(self):
        self.assertEqual(ade_fetcher.get_student_id('alfloch001'), 5609)

    def test_get_room_id(self):
        self.assertEqual(ade_fetcher.get_room_id('AMPHI A'), 3216)
        self.assertEqual(ade_fetcher.get_room_id('AMPHI E'), 3220)
        self.assertEqual(ade_fetcher.get_room_id('E117'), 3262)
        self.assertEqual(ade_fetcher.get_room_id('I007'), 3235)
        self.assertEqual(ade_fetcher.get_room_id('P201'), 3333)

    def test_parse_planning(self):
        with open('planning.ics', 'r') as file:
            planning = ade_fetcher.parse_planning(file.read())

            self.assertEqual(len(planning.events), 3)
            self.assertEqual(planning.day_duration().seconds / 3600, 6)

            event1, event2, event3 = planning.events
            self.assertEqual(
                event1.start, datetime.datetime(
                    2023, 9, 27, 10, 20))
            self.assertEqual(
                event1.end, datetime.datetime(
                    2023, 9, 27, 12, 20))
            self.assertEqual(event1.summary, 'Cours A')
            self.assertEqual(event1.room, 'S117/S118 - TD12')

            self.assertEqual(
                event2.start, datetime.datetime(
                    2023, 9, 27, 14, 0))
            self.assertEqual(
                event2.end, datetime.datetime(
                    2023, 9, 27, 15, 20))
            self.assertEqual(event2.summary, 'Cours B')
            self.assertEqual(event2.room, 'AMPHI E')

            self.assertEqual(
                event3.start, datetime.datetime(
                    2023, 9, 27, 15, 30))
            self.assertEqual(
                event3.end, datetime.datetime(
                    2023, 9, 27, 16, 20))
            self.assertEqual(event3.summary, 'Cours C')
            self.assertEqual(event3.room, 'AMPHI E')


if __name__ == '__main__':
    unittest.main()
