from ade_enseirb import ADEClient

from getpass import getpass
import datetime
import sys

start, end = datetime.datetime.now(), datetime.datetime.now()

username = input('Username: ')
ade_client = ADEClient(username, getpass("Enter your CAS password: "))


def date_to_str(date):
    return date.strftime('%A %d %B %Y')


def get_day_duration(planning):
    return (planning.last_event().end - planning.first_event().start).total_seconds() / 60


def get_day_advance(planning):
    minutes_passed = (datetime.datetime.now() - planning.first_event().start).total_seconds() / 60
    return max(min(minutes_passed / get_day_duration(planning), 1), 0)


def progress_bar(planning, width):
    advance = get_day_advance(planning)
    progress = int(advance * width)
    progress_chars = [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
    progress_bar = '█' * progress
    if progress < width:
        progress_bar += progress_chars[int((advance * width - progress) * 9)]
    progress_bar += ' ' * (width - progress - 1)
    if advance == 1:
        return '\033[1m\033[32m' + progress_bar + '\033[0m'
    return '\033[1m\033[31m' + progress_bar + '\033[0m'


def pretty_print_planning(planning):
    table_width = 79
    room_length = 16
    hour_length = 13

    content_length = table_width - hour_length - 4 - 2 - room_length - 4
    date_length = table_width - hour_length - 4 - 2

    # Header
    print('╒═══════════════╤═' + '═' * content_length + '═══' + '═' * room_length + '═╕')
    print('│ ', end='')
    print(progress_bar(planning, hour_length) + ' │ ', end='')
    day = date_to_str(planning.events[0].start)
    day = day[:date_length]
    padding = (date_length - len(day)) // 2
    extra_padding = (date_length - len(day)) % 2
    print(' ' * padding, end='')
    print('\033[1m' + day + '\033[0m', end='')
    print(' ' * (padding + extra_padding), end='')
    print('│')

    print('╞═══════════════╪═', end='')
    print('═' * content_length, end='')
    print('═╤═' + '═' * room_length + '═╡')

    # Body
    for k, event in enumerate(planning.events):
        print('│ ', end='')
        start = event.start.time().strftime('%H:%M')
        end = event.end.time().strftime('%H:%M')
        text = start + ' - ' + end
        if event.is_passed():
            print(f'\033[9m{text}\033[0m', end='')
        if event.is_now():
            print(f'\033[1m\033[31m{text}\033[0m', end='')
        elif event.is_incoming():
            print(f'\033[1m\033[34m{text}\033[0m', end='')
        print(' │ ', end='')

        summary = event.summary
        summary = summary[:content_length]
        print(summary, end='')
        print(' ' * (content_length - len(summary)), end='')
        print(' │ ', end='')

        room = event.room

        room = room[:room_length]
        print(f'\033[1m{room}\033[0m', end='')
        print(' ' * (room_length - len(room)), end='')
        print(' │')
        if k != len(planning.events) - 1:
            print('├───────────────┼─', end='')
            print('─' * content_length, end='')
            print('─┼─' + '─' * room_length + '─┤')

    # End
    print('╘═══════════════╧═', end='')
    print('═' * content_length, end='')
    print('═╧═' + '═' * room_length + '═╛')


def pretty_print_days(username, start, end):
    for day in range((end - start).days + 1):
        day = start + datetime.timedelta(days=day)
        planning = ade_client.student_day_planning(username, day.strftime('%Y-%m-%d'))
        if planning.event_count() == 0:
            print(f'No event on {date_to_str(day)}')
            continue
        pretty_print_planning(planning)

# Parse an argument among the following
# -t means tommorow
# -n means next day
# -w means whole week
# -u means only upcoming events


if len(sys.argv) == 1:
    current_day = datetime.datetime.now()
    pretty_print_days(username, current_day, current_day)
else:
    arg = sys.argv[1]
    if arg == '-t':
        day = datetime.datetime.now() + datetime.timedelta(days=1)
        pretty_print_days(username, day, day)
    elif arg == '-n':
        day = datetime.datetime.now() + datetime.timedelta(days=1)
        if day.weekday() >= 6:
            day = day + datetime.timedelta(days=7 - day.weekday() + 1)
        pretty_print_days(username, day, day)
    elif arg == '-w':
        current_day = datetime.datetime.now()
        start_of_week = current_day - datetime.timedelta(days=current_day.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=4)
        pretty_print_days(username, start_of_week, end_of_week)
    else:
        print('Unknown argument', arg)
