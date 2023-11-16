import datetime
import pytz
from tzlocal import get_localzone


def next_working_day():
    current_date = datetime.datetime.now()
    weekday = current_date.weekday()
    if weekday >= 5:
        return current_date + datetime.timedelta(days=7 - weekday + 1)
    return current_date + datetime.timedelta(days=1)


def first_day_of_week():
    current_date = datetime.datetime.now()
    return current_date - datetime.timedelta(days=current_date.weekday())


def last_day_of_week():
    current_date = datetime.datetime.now()
    days_before_end_of_week = 6 - current_date.weekday()
    return current_date + datetime.timedelta(days=days_before_end_of_week)


def convert_date(date):
    """
    Turns YYYY MM DD T HH MM SS into a datetime object
    This also changes the hour to match the french timezone
    """
    datetime_utc = datetime.datetime.strptime(date, '%Y%m%dT%H%M%SZ').replace(tzinfo=pytz.UTC)
    local_datetime = datetime_utc.astimezone(get_localzone())
    return local_datetime.replace(tzinfo=None)


class Event:

    __slots__ = ['start', 'end', 'summary', 'room']

    def __init__(self, start, end, summary, room):
        self.start = start
        self.end = end
        self.summary = summary
        self.room = room

    def __str__(self):
        day = self.start.date().strftime('%d/%m/%Y')
        start = self.start.time().strftime('%Hh%M')
        end = self.end.time().strftime('%Hh%M')
        return f'[{day}] {start} - {end} {self.summary} ({self.room})'

    def duration(self) -> datetime.timedelta:
        """
        Returns:
            datetime.timedelta: Duration of the event.
        """
        return self.end - self.start

    def is_now(self) -> bool:
        """
        Returns:
            bool: True if the event is happening now.
        """
        return self.start < datetime.datetime.now() < self.end

    def is_passed(self) -> bool:
        """
        Returns:
            bool: True if the event is passed.
        """
        return datetime.datetime.now() >= self.end

    def is_incoming(self) -> bool:
        """
        Returns:
            bool: True if the event is incoming.
        """
        return datetime.datetime.now() <= self.start


class Planning:

    __slots__ = ['events']

    def __init__(self):
        self.events = []

    def __str__(self):
        result = ''
        for k, event in enumerate(self.events):
            result += str(event)
            if k != len(self.events) - 1:
                result += '\n'
        return result

    def _add_event(self, start: datetime.datetime, end: datetime.datetime, summary: str, location: str):
        """
        Args:
            start (datetime.datetime): Start of the event.
            end (datetime.datetime): End of the event.
            summary (str): Summary of the event.
            location (str): Location of the event.

        Raises:
            ValueError: If the event is not in chronological order.
        """
        new_event = Event(start, end, summary, location)
        for k, event in enumerate(self.events):
            if new_event.start < event.start:
                self.events.insert(k, new_event)
                return
        self.events.append(new_event)

    def event_count(self) -> int:
        """
        Returns:
            int: Number of events in the planning.
        """
        return len(self.events)

    def first_event(self) -> Event:
        """
        Returns:
            Event: First event of the planning.

        Raises:
            ValueError: If no event is found.
        """
        if len(self.events) == 0:
            raise ValueError('No event found')
        return self.events[0]

    def start_of_first_event(self) -> datetime.datetime:
        """
        Returns:
            datetime.datetime: Start time of the first event of the planning.

        Raises:
            ValueError: If no event is found.
        """
        return self.first_event().start

    def last_event(self) -> Event:
        """
        Returns:
            Event: Last event of the planning.

        Raises:
            ValueError: If no event is found.
        """
        if len(self.events) == 0:
            raise ValueError('No event found')
        return self.events[-1]

    def end_of_last_event(self) -> datetime.datetime:
        """
        Returns:
            datetime.datetime: End time of the last event of the planning.

        Raises:
            ValueError: If no event is found.
        """
        return self.last_event().end

    def events_done(self) -> int:
        """
        Returns:
            int: Number of events done in a day
        """
        result = 0
        for event in self.events:
            result += event.is_passed()
        return result

    def day_duration(self) -> datetime.timedelta:
        """
        Returns:
            datetime.timedelta: Duration between the first and last event.
                This function makes sense only if events are on the same day.
        """
        if len(self.events) == 0:
            return datetime.timedelta()
        return self.events[-1].end - self.events[0].start

    def work_duration(self) -> datetime.timedelta:
        """
        Returns:
            datetime.timedelta: Duration of all events in the planning.
        """
        total = datetime.timedelta()
        for event in self.events:
            total += event.duration()
        return total

    def event_running(self) -> Event:
        """
        Returns:
            Event: Event that is running now.
                If no event is running, returns None.
        """
        for event in self.events:
            if event.is_now():
                return event
        return None
