import curses
import datetime
import time
from ade_enseirb import ADEClient

CAS_text = [
    "  ██████╗ █████╗ ███████╗ ",
    " ██╔════╝██╔══██╗██╔════╝ ",
    " ██║     ███████║███████╗ ",
    " ██║     ██╔══██║╚════██║ ",
    " ╚██████╗██║  ██║███████║ ",
    "  ╚═════╝╚═╝  ╚═╝╚══════╝ "
]

ade_client = None
ade_username = None
login_tries = 0


def date_to_str(date):
    return date.strftime('%A %d %B %Y')


def login(stdscr, error=None):
    global ade_client, ade_username, login_tries

    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    y = height // 2

    text_y = y - len(CAS_text) // 2
    padding = 3
    x_offset = len(CAS_text[0]) + 2 + 2 * padding

    cas_win = curses.newwin(height, x_offset, 0, 0)
    cas_win.border()
    for i, line in enumerate(CAS_text):
        cas_win.addstr(text_y + i, 1 + padding, line)
    cas_win.refresh()

    form_win = curses.newwin(height, width - x_offset, 0, x_offset)
    form_win.border()
    form_win.refresh()

    username = curses.newwin(1, 16, y - 2, x_offset + (width - x_offset) // 2 - 2)
    password = curses.newwin(1, 16, y + 0, x_offset + (width - x_offset) // 2 - 2)

    if error is not None:
        text_height, text_width = 1, len(error) + 2
        err = curses.newwin(text_height, text_width, height - 3, x_offset + (width - x_offset) // 2 - text_width // 2)
        err.addstr(0, 0, error)
        err.refresh()

    stdscr.addstr(y - 2, x_offset + (width - x_offset) // 2 - 12, "Username:")
    stdscr.addstr(y, x_offset + (width - x_offset) // 2 - 12, "Password:")

    stdscr.refresh()

    curses.echo()

    ade_username = username.getstr(0, 0, 20).decode("utf-8")

    # Disable echoing for password input
    curses.noecho()

    password.move(0, 0)
    password.refresh()
    password_input = password.getstr(0, 0, 20).decode("utf-8")

    try:
        ade_client = ADEClient(ade_username, password_input)
        display_plannings(stdscr)
    except BaseException:
        login_tries += 1
        if login_tries >= 3:
            exit(1)
        login(stdscr, error=f"Try again ({login_tries} / 3)")


def display_plannings(stdscr):
    global ade_client, ade_username

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    height, width = stdscr.getmaxyx()
    x = width // 2

    def build_planning(day, x_offset=0):
        planning = ade_client.student_day_planning(ade_username, day)
        win = curses.newwin(height, x, 0, x_offset)
        win.border()

        if len(planning.events) == 0:
            win.addstr(3, 1, '┌' + '─' * (x - 4) + '┐')
            win.addstr(4, 1, '│')
            win.addstr(4, x // 2 - 4, 'No class')
            win.addstr(4, x - 2, '│')
            win.addstr(5, 1, '└' + '─' * (x - 4) + '┘')
            win.refresh()
        else:
            win.addstr(3, 1, '┌' + '─' * (x - 4) + '┐')
            for k, event in enumerate(planning.events):
                start = event.start.time().strftime('%Hh%M')
                end = event.end.time().strftime('%Hh%M')
                time = start + ' - ' + end
                room = event.room
                room = room[:x - 6 - len(time) - 2]
                summary = event.summary[:x - 6]
                summary_x = x // 2 - len(summary) // 2

                time_color = curses.color_pair(3)
                if event.is_incoming():
                    time_color = curses.color_pair(2) | curses.A_BOLD
                elif event.is_now():
                    time_color = curses.color_pair(3) | curses.A_BOLD
                win.addstr(4 + 3 * k, 1, '│')
                win.addstr(4 + 3 * k, 3, time, time_color)
                win.addstr(4 + 3 * k, x - 3 - len(room), room, curses.color_pair(1) | curses.A_BOLD)
                win.addstr(4 + 3 * k, x - 2, '│')

                win.addstr(4 + 3 * k + 1, 1, '│')
                win.addstr(4 + 3 * k + 1, summary_x, summary)
                win.addstr(4 + 3 * k + 1, x - 2, '│')

                if k != len(planning.events) - 1:
                    win.addstr(4 + 3 * k + 2, 1, '├' + '─' * (x - 4) + '┤')

            win.addstr(4 + 3 * (len(planning.events) - 1) + 2, 1, '└' + '─' * (x - 4) + '┘')

            win.refresh()

        title = curses.newwin(2, x - 2, 1, x_offset + 1)
        title_text = date_to_str(day)
        title_x = x // 2 - len(title_text) // 2
        title.addstr(0, title_x, title_text, curses.color_pair(4) | curses.A_BOLD)
        title.addstr(1, title_x, '─' * len(title_text))
        title.refresh()

    build_planning(datetime.datetime.now().date(), x_offset=0)
    build_planning(datetime.datetime.now().date() + datetime.timedelta(days=1), x_offset=x)

    day_offset = 0
    while True:
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            day_offset -= 1
        elif key == curses.KEY_UP:
            day_offset -= 7
        elif key == curses.KEY_RIGHT:
            day_offset += 1
        elif key == curses.KEY_DOWN:
            day_offset += 7
        elif key == ord('q'):
            exit(0)

        if key in [curses.KEY_LEFT, curses.KEY_UP, curses.KEY_RIGHT, curses.KEY_DOWN]:
            stdscr.clear()
            stdscr.refresh()
            build_planning(datetime.datetime.now().date() + datetime.timedelta(days=day_offset))
            build_planning(datetime.datetime.now().date() + datetime.timedelta(days=day_offset + 1), x_offset=x)

        time.sleep(0.1)


def main(stdscr):
    stdscr.nodelay(True)
    stdscr.keypad(True)
    login(stdscr)

    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
