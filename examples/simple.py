from ade_enseirb import ADEClient

from getpass import getpass
import datetime


user = input('Username: ')
ade_client = ADEClient(user, getpass())

# CF .rooms.json or ade_client.rooms_list() to get the list of rooms
room = 'AMPHI E'

start, end = datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=7)

print(f'Planning of {room}:')
print(ade_client.room_planning(room, start, end))
print(f'Planning of {room} (today):')
print(ade_client.room_day_planning(room, start))
print()

print(f'Planning of {user}:')
print(ade_client.student_planning(user, start, end))
print(f'Planning of {user} (today):')
print(ade_client.student_day_planning(user, start))
print(f'Planning of {user} (this week):')
print(ade_client.student_week_planning(user))
print(f'Planning of {user} (this week, from monday):')
print(ade_client.student_week_planning(user, from_monday=True))
print()

# Unoptimized, each call require a request to the website
# This should be used only if you need one of these calls
print(ade_client.day_duration(user))
print(ade_client.work_duration(user))
print(ade_client.event_count(user))
print(ade_client.events_done(user))
print(ade_client.start_of_first_event(user))
print(ade_client.end_of_last_event(user))
print(ade_client.first_event(user))
print(ade_client.last_event(user))
print()

# Optimized, every call is fast as the request is done only once
planning = ade_client.student_day_planning(user)
print(planning.day_duration())
print(planning.work_duration())
print(planning.event_count())
print(planning.events_done())
print(planning.start_of_first_event())
print(planning.end_of_last_event())
print(planning.first_event())
print(planning.last_event())

# Other calls, uncomment to test
# print()
# print(ade_client.rooms_list())
# print(ade_client.rooms_id())
