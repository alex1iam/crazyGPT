# Определяем класс Device
class Device:
    def __init__(self, device_id, main_topic, name, location, commands, status, sending):
        self.device_id = device_id
        self.main_topic = main_topic
        self.name = name
        self.location = location
        self.commands = commands
        self.status = status
        self.sending = sending

devices = {
    "id1": Device(
        device_id="id1",
        main_topic='input',
        name='свет',
        location='прихожая',
        commands={
            '/light_z1_on_off': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                },
            '/light_z1_brightness': {
                ('ярче', 'светлее'): '{"+1"}',
                ('тусклее', 'темнее'): '{"-1"}',
            },
        },
        status='',
        sending=''
    ),
    "id2": Device(
        device_id="id2",
        main_topic='input',
        name='свет',
        location='зал',
        commands={
            '/light_z2_on_off': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                },
            '/light_z2_brightness': {
                ('ярче', 'светлее'): '{"+1"}',
                ('тусклее', 'темнее'): '{"-1"}',
            },
        },
        status='',
        sending=''
    ),
    "id3": Device(
        device_id="id3",
        main_topic='input',
        name='люстра',
        location='зал',
        commands={
            '/light_z3_on_off': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                },
            '/light_z3_brightness': {
                ('ярче', 'светлее'): '{"+1"}',
                ('тусклее', 'темнее'): '{"-1"}',
            },
        },
        status='',
        sending=''
    ),
    "id4": Device(
        device_id="id4",
        main_topic='input',
        name='свет',
        location='кухня',
        commands={
            '/light_z4_on_off': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                },
            '/light_z4_brightness': {
                ('ярче', 'светлее'): '{"+1"}',
                ('тусклее', 'темнее'): '{"-1"}',
            },
        },
        status='',
        sending=''
    ),
    "id5": Device(
        device_id="id5",
        main_topic='zigbee2mqtt/0x00158d0002c99665',
        name='свет',
        location='ванная',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id6": Device(
        device_id="id6",
        main_topic='zigbee2mqtt/0x00158d00029b5e24',
        name='лампа',
        location='кухня',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id7": Device(
        device_id="id7",
        main_topic='zigbee2mqtt/0x00158d00045c8acc',
        name='свет',
        location='ниша',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id8": Device(
        device_id="id8",
        main_topic='zigbee2mqtt/0x847127fffed08e8a',
        name='штора слева',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'OPEN',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'CLOSE',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id9": Device(
        device_id="id9",
        main_topic='zigbee2mqtt/0xb4e3f9fffe07d38e',
        name='штора в центре',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'OPEN',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'CLOSE',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id10": Device(
        device_id="id10",
        main_topic='zigbee2mqtt/0xb4e3f9fffe07cfa4',
        name='штора справа',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'OPEN',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'CLOSE',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id11": Device(
        device_id="id11",
        main_topic='zigbee2mqtt/0xb43522fffe984d83',
        name='штора слева',
        location='кухня',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'OPEN',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'CLOSE',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id12": Device(
        device_id="id12",
        main_topic='zigbee2mqtt/0x048727fffe5629c6',
        name='штора справа',
        location='кухня',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'OPEN',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'CLOSE',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id13": Device(
        device_id="id13",
        main_topic='zigbee2mqtt/0xa4c138584ebe639b',
        name='горячая вода',
        location='ванная',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id14": Device(
        device_id="id14",
        main_topic='zigbee2mqtt/0xa4c138584ebe639b',
        name='холодная вода',
        location='ванная',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id15": Device(
        device_id="id15",
        main_topic='zigbee2mqtt/0xa4c138d99e6fe4ee',
        name='розетка',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id16": Device(
        device_id="id16",
        main_topic='zigbee2mqtt/0xa4c138cfad634dcf/l1',
        name='свет справа',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id17": Device(
        device_id="id17",
        main_topic='zigbee2mqtt/0xa4c138cfad634dcf/l2',
        name='свет один',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id18": Device(
        device_id="id18",
        main_topic='zigbee2mqtt/0xa4c138cfad634dcf/l3',
        name='свет два',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),
    "id19": Device(
        device_id="id19",
        main_topic='zigbee2mqtt/0xa4c138cfad634dcf/l4',
        name='свет слева',
        location='зал',
        commands={
            '': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй', 'открой'): 'ON',
                ('выключи', 'выруби', 'грохни', 'закрой'): 'OFF',
            },
        },
        status='/state',
        sending='/set'
    ),


}

groups = {
    "свет": ["id16", "id17", "id18", "id19"],
#    "свет": ["id1", "id2", "id3", "id4", "id5", "id6", "id7"],
    "шторы зал": ["id8", "id9", "id10"],
    "шторы кухня": ["id11", "id12"],
    "шторы": ["id8", "id9", "id10", "id11", "id12"],
#    "все": ["id1", "id2", "id3", "id4", "id5", "id6", "id7", "id8", "id9", "id10", "id11", "id12"]
    "все": ["id1", "id3", "id8", "id12"]
}
