from bs4 import BeautifulSoup
import requests


class CASClient:

    __slots__ = ['username', 'password', 'session']

    _header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.session = requests.Session()

    def login(self) -> None:
        login_url = 'https://cas.bordeaux-inp.fr/login'

        response = self.session.get(login_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        payload = {
            'username': self.username,
            'password': self.password,
            'execution': soup.find('input', {'name': 'execution'})['value'],
            '_eventId': 'submit',
        }

        self.session.post(
            response.url,
            headers=CASClient._header,
            data=payload)

        ade_url = 'https://ade.bordeaux-inp.fr/direct/myplanning.jsp'

        # If redirected, login failed
        if login_url in self.session.get(ade_url).url:
            raise ValueError('Wrong credentials')

    def get_session(self) -> requests.Session:
        return self.session

    def close_session(self) -> None:
        self.session.close()
