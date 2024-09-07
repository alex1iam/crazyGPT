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
        main_topic='zigbee2mqtt/0xa4c138d99e6fe4ee',
        name='розетка',
        location='зал',
        commands={
            '/': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                ('закрой', 'заблокируй', 'запри'): '{"child_lock": "LOCK"}',  # Новое действие
                ('открой', 'разблокируй', 'отопри'): '{"child_lock": "UNLOCK"}',  # Новое действие
            },
        },
        status='/state',
        sending='set'
    ),
    "id2": Device(
        device_id="id2",
        main_topic='zigbee2mqtt/0xa4c138d99e6fe4ee/id2',
        name='свет слева',
        location='зал',
        commands={
            '/': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                ('закрой', 'заблокируй', 'запри'): '{"child_lock": "LOCK"}',  # Новое действие
                ('открой', 'разблокируй', 'отопри'): '{"child_lock": "UNLOCK"}',  # Новое действие
                ('ярче', 'светлее'): '{"+1"}',
                ('тусклее', 'темнее'): '{"-1"}',
            },
        },
        status='/state',
        sending='set'
    ),
    "id3": Device(
        device_id="id3",
        main_topic='zigbee2mqtt/0xa4c138d99e6fe4ee/id3',
        name='телек',
        location='кухня',
        commands={
            '/': {  # Команды управления состоянием
                ('включи', 'вруби', 'задействуй'): 'ON',
                ('выключи', 'выруби', 'грохни'): 'OFF',
                ('ярче', 'светлее'): '{"+1"}',
                ('тусклее', 'темнее'): '{"-1"}',
                ('громче', 'сильнее'): '{"+1"}',
                ('тише', 'слабее'): '{"-1"}',
            },
        },
        status='/state',
        sending='set'
    ),
}

groups = {
    "свет": ["id1", "id3"],  # Включаем id2 (свет) и id3 (лампа)
    "электрика": ["id1", "id2"],  # Включаем id1 (розетка) и id2 (свет)
    "уборка": ["id2", "id3"]  # Можно оставить пустым для будущих добавлений
}
