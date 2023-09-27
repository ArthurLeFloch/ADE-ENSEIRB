from ade_enseirb.cas import CASClient

import unittest
from getpass import getpass


class TestCasAuthentication(unittest.TestCase):

    def test_login(self):
        client = CASClient(input('Username: '), getpass())
        client.login()

        ade_url = 'https://ade.bordeaux-inp.fr/direct/myplanning.jsp'
        self.assertEqual(client.session.get(ade_url).url, ade_url)

        client.close_session()

    def test_bad_login(self):
        client = CASClient('login', 'password')

        self.assertRaises(ValueError, client.login)

        client.close_session()


if __name__ == '__main__':
    unittest.main()
