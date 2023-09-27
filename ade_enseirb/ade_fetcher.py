from .utils import Planning, convert_date

import json
import re
import datetime

timestamp = str(datetime.datetime.now())


def fix_room(room):
    room = room.replace('EA-', '')
    room = room.replace('EB-', '')
    pattern = r'(.*) \((.*)\)'
    room = re.sub(pattern, r'\1 - \2', room)
    room = room.strip()
    if room.startswith('- '):
        room = room[2:]
    return room


class ADEFetcher:

    __slots__ = ['_session', '_rooms_id']

    _ade_header = {
        'Content-Type': 'text/x-gwt-rpc; charset=UTF-8',
        'X-GWT-Module-Base': 'https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/',
        'X-GWT-Permutation': 'B6FB4BD1F96498A84974F1F52B318B82'
    }

    _rooms_file = '.rooms.json'

    _unused_tokens = [
        'METHOD',
        'PRODID',
        'VERSION',
        'CALSCALE',
        'BEGIN:VCALENDAR',
        'END:VCALENDAR',
        'END:VEVENT',
        'SEQUENCE',
        'LAST-MODIFIED',
        'DTSTAMP',
        'CREATED',
        'UID',
        'DESCRIPTION',
        ' '
    ]

    def __init__(self, cas_session):
        self._session = cas_session
        self._rooms_id = {}

    def connect(self):
        url = 'https://ade.bordeaux-inp.fr/direct/myplanning.jsp'
        self._session.get(url)

        url = 'https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/MyPlanningClientServiceProxy'
        payload = f"7|0|8|https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/|217140C31DF67EF6BA02D106930F5725|com.adesoft.gwt.directplan.client.rpc.MyPlanningClientServiceProxy|method1login|J|com.adesoft.gwt.core.client.rpc.data.LoginRequest/3705388826|com.adesoft.gwt.directplan.client.rpc.data.DirectLoginRequest/635437471||1|2|3|4|2|5|6|{timestamp}|7|0|0|0|1|1|8|8|-1|0|0|"
        self._session.post(url, headers=ADEFetcher._ade_header, data=payload)

        url = "https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/WebClientServiceProxy"
        payload = f"7|0|7|https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/|34BFB581389200AE2C2012C5A7E57F95|com.adesoft.gwt.core.client.rpc.WebClientServiceProxy|method6loadProject|J|I|Z|1|2|3|4|3|5|6|7|{timestamp}|1|0|"
        self._session.post(url, headers=ADEFetcher._ade_header, data=payload)

    def load_data(self):
        try:
            with open(ADEFetcher._rooms_file, 'r') as file:
                self._rooms_id = json.load(file)
        except BaseException:
            self._fetch_rooms()

    def _load_folder(self, path, name, id, depth, weird_codes):
        id = str(id)
        depth = str(depth)
        url = "https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/DirectPlanningServiceProxy"
        payload = '7|0|20|https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/|067818807965393FC5DCF6AECC2CA8EC|com.adesoft.gwt.directplan.client.rpc.DirectPlanningServiceProxy|method4getChildren|J|java.lang.String/2004016611|com.adesoft.gwt.directplan.client.ui.tree.TreeResourceConfig/2234901663|{"' + id + '""true""' + depth + '""' + weird_codes[0] + '""false"[2]{"ColorField""COLOR""LabelColor""255,255,255""false""false"{"StringField""NAME""LabelName""' + name + '""false""false""' + path + '""' + weird_codes[1] + '""0"[0][0]|[I/2970817851|java.util.LinkedHashMap/3008245022|COLOR|com.adesoft.gwt.core.client.rpc.config.OutputField/870745015|LabelColor||com.adesoft.gwt.core.client.rpc.config.FieldType/1797283245|NAME|LabelName|java.util.ArrayList/4159755760|com.extjs.gxt.ui.client.data.SortInfo/1143517771|com.extjs.gxt.ui.client.Style$SortDir/3873584144|1|2|3|4|3|5|6|7|' + timestamp + '|8|7|0|9|2|-1|-1|10|0|2|6|11|12|0|13|11|14|15|11|0|0|6|16|12|0|17|16|14|15|4|0|0|18|0|18|0|19|20|1|16|18|0|'
        response = self._session.post(url, headers=ADEFetcher._ade_header, data=payload)
        pattern = r'{\\"(\d+)(?:\\"){2}(true|false).*?\\"LabelName(?:\\"){2}([(\w|\-/)_ ]+)'
        return re.findall(pattern, response.text)

    def _fetch_rooms(self):
        weird_codes = ['-1""5""5""0', 'classroom""3']
        folders = self._load_folder('ENSEIRB-MATMECA', 'ENSEIRB-MATMECA', 3091, 1, weird_codes)
        for room_id, is_folder, room_name in folders:
            if is_folder == 'false':
                room_name = fix_room(room_name)
                self._rooms_id[room_name] = int(room_id)
        with open(ADEFetcher._rooms_file, 'w') as file:
            json.dump(self._rooms_id, file, indent=4)

    def get_student_id(self, username):
        url = "https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/DirectPlanningServiceProxy"
        payload = f"7|0|13|https://ade.bordeaux-inp.fr/direct/gwtdirectplanning/|067818807965393FC5DCF6AECC2CA8EC|com.adesoft.gwt.directplan.client.rpc.DirectPlanningServiceProxy|method7getResourceIds|J|java.util.List|java.util.Map|Z|java.util.ArrayList/4159755760|java.util.HashMap/1797211028|com.adesoft.gwt.directplan.client.rpc.ResourceFieldCriteria/1324434193|java.lang.String/2004016611|{username}|1|2|3|4|4|5|6|7|8|{timestamp}|9|0|10|1|11|17|9|1|12|13|0|"
        response = self._session.post(url, headers=ADEFetcher._ade_header, data=payload)
        pattern = r'\[(\d+)'
        result = re.findall(pattern, response.text)[0]
        if result != '0':
            return int(result)
        raise Exception(f'User {username} not found')

    def get_room_id(self, room):
        if room in self._rooms_id:
            return self._rooms_id[room]
        raise Exception(f'Room {room} not found')

    def parse_planning(self, planning):
        useful_data = []
        for line in planning.split('\n'):
            if not any(line.startswith(token) for token in ADEFetcher._unused_tokens):
                useful_data.append(line)

        result = Planning()
        for course in re.split(r'BEGIN:VEVENT', '\r'.join(useful_data)):
            if course == '':
                continue
            start, end, summary, room = None, None, None, None
            for line in course.split('\r'):
                if line == '':
                    continue
                content = line.split(':')[1]
                if line.startswith('DTSTART'):
                    start = convert_date(content)
                elif line.startswith('DTEND'):
                    end = convert_date(content)
                elif line.startswith('SUMMARY'):
                    summary = content
                elif line.startswith('LOCATION'):
                    room = fix_room(content)
            if room != '':
                result._add_event(start, end, summary, room)
        return result

    def get_planning(self, id, start, end):
        url = f'https://adeapp.bordeaux-inp.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources={id}&projectId=1&calType=ical&firstDate={start}&lastDate={end}&displayConfigId=71'
        return self.parse_planning(self._session.get(url).text)

    def get_room_list(self):
        return list(self._rooms_id.keys())

    def get_room_id_list(self):
        result = {}
        for room in self._rooms_id:
            result[room] = self._rooms_id[room]
        return result
