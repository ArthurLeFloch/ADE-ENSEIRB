from .ade_fetcher import ADEFetcher
from .cas import CASClient
from .utils import Event, Planning, next_working_day, first_day_of_week, last_day_of_week

import datetime


class ADEClient:

    __slots__ = ['fetcher']

    def __init__(self, username: str, password: str) -> None:
        """
        Initializes an ADE client, which connects to Bordeaux INP's CAS
        with provided credentials, and fetches data from ADE.

        Args:
            username (str): CAS username of the user.
            password (str): CAS password of the user.

        Raises:
            ValueError: If the connection to CAS failed.
        """
        cas_client = CASClient(username, password)
        cas_client.login()

        self.fetcher = ADEFetcher(cas_client.get_session())
        self.fetcher.connect()
        self.fetcher.load_data()

    ###########
    #  ROOMS  #
    ###########
    def rooms_list(self) -> list:
        """
        Returns:
            list: List of all room names.
        """
        return self.fetcher.get_room_list()

    def rooms_id(self) -> dict:
        """
        Returns:
            dict: Dictionary of all room names and their ADE IDs.
        """
        return self.fetcher.get_room_id_list()

    def room_planning(self, room, start: str, end: str) -> Planning:
        """
        Args:
            room (str or int): Room name or ADE ID of the room.
            start (str): Start date of the planning (YYYY-MM-DD).
            end (str): End date of the planning (YYYY-MM-DD).

        Returns:
            Planning: Room's planning between the two dates.
        """
        if isinstance(room, int):
            return self.fetcher.get_planning(room, start, end)
        elif isinstance(room, str):
            room_id = self.fetcher.get_room_id(room)
            return self.fetcher.get_planning(room_id, start, end)
        raise TypeError('"room" must be a string (room name) or int (ADE ID)')

    def room_day_planning(self, room, day=None) -> Planning:
        """
        Args:
            room (str or int): Room name or ADE ID of the room.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            Planning: Room's planning for the day.
        """
        if day is None:
            day = datetime.datetime.now().strftime('%Y-%m-%d')
        return self.room_planning(room, day, day)

    def room_next_day_planning(self, room) -> Planning:
        """
        Args:
            room (str or int): Room name or ADE ID of the room.

        Returns:
            Planning: Room's planning for the next working day.
        """
        day = next_working_day().strftime('%Y-%m-%d')
        return self.room_planning(room, day, day)

    ##############
    #  STUDENTS  #
    ##############
    def student_planning(self, student, start: str, end: str) -> Planning:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            start (str): Start date of the planning (YYYY-MM-DD).
            end (str): End date of the planning (YYYY-MM-DD).

        Returns:
            Planning: Student's planning between the two dates.
        """
        if isinstance(student, int):
            return self.fetcher.get_planning(student, start, end)
        elif isinstance(student, str):
            student_id = self.fetcher.get_student_id(student)
            return self.fetcher.get_planning(student_id, start, end)
        raise TypeError('"student" must be a string (username) or int (ADE ID)')

    def student_day_planning(self, student, day=None) -> Planning:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            Planning: Student's planning for the day.
        """
        if day is None:
            day = datetime.datetime.now().strftime('%Y-%m-%d')
        return self.student_planning(student, day, day)

    def student_next_day_planning(self, student) -> Planning:
        """
        Args:
            student (str or int): Username or ADE ID of the student.

        Returns:
            Planning: Student's planning for the next working day.
        """
        day = next_working_day().strftime('%Y-%m-%d')
        return self.student_planning(student, day, day)

    def student_week_planning(self, student, from_monday=False) -> Planning:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            from_monday (bool): Whether data should be fetched from monday
                instead of the current day.

        Returns:
            Planning: Student's planning for the current week.
        """
        start = datetime.datetime.now()
        if from_monday:
            start = first_day_of_week()
        start = start.strftime('%Y-%m-%d')
        end = last_day_of_week().strftime('%Y-%m-%d')
        return self.student_planning(student, start, end)

    ##################
    #  MISCELANEOUS  #
    ##################
    def event_count(self, student, day=None) -> int:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            int: Number of events in the planning.
        """
        return len(self.student_day_planning(student, day).events)

    def first_event(self, student, day=None) -> Event:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            Event: First event of the planning.
        """
        return self.student_day_planning(student, day).first_event()

    def start_of_first_event(self, student, day=None) -> datetime.datetime:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            datetime.datetime: Start time of the first event in the planning.
        """
        return self.first_event(student, day).start

    def last_event(self, student, day=None) -> Event:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            Event: Last event of the planning.
        """
        return self.student_day_planning(student, day).last_event()

    def end_of_last_event(self, student, day=None) -> datetime.datetime:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            datetime.datetime: End time of the last event of the planning.
        """
        return self.last_event(student, day).end

    def events_done(self, student, day=None) -> int:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            int: Number of events done in a day.
        """
        result = 0
        for event in self.student_day_planning(student, day).events:
            result += event.is_passed()
        return result

    def day_duration(self, student, day=None) -> datetime.timedelta:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            datetime.timedelta: Duration between the first and last
                event in a day.
        """
        planning = self.student_day_planning(student, day)
        if len(planning.events) == 0:
            return datetime.timedelta()
        return planning.events[-1].end - planning.events[0].start

    def work_duration(self, student, day=None) -> datetime.timedelta:
        """
        Args:
            student (str or int): Username or ADE ID of the student.
            day (str or None): Date of the planning (YYYY-MM-DD).
                If None, the current day is used.

        Returns:
            datetime.timedelta: Total duration of the events in a day.
        """
        total = datetime.timedelta()
        for event in self.student_day_planning(student, day).events:
            total += event.end - event.start
        return total

    def event_running(self, student) -> Event:
        """
        Args:
            student (str or int): Username or ADE ID of the student.

        Returns:
            Event: Event that is running now.
                If no event is running, returns None.
        """
        for event in self.student_day_planning(student).events:
            if event.is_running():
                return event
        return None
