import paho.mqtt.client as mqtt
from fuzzywuzzy import fuzz
import sounddevice as sd
import soundfile as sf
import configparser
import numpy as np
import threading
import queue
import vosk
import json

# Конфигурация
device_m = 1
model = vosk.Model("model_stt/vosk-model-small-ru-0.22")
samplerate = 44100
q = queue.Queue()

# Чтение конфигураций
config = configparser.ConfigParser()
config.read('./settings.ini')

IP = config['MQTT']['ip']
PORT = int(config['MQTT']['port'])
WAKE_STRING = config['WAKE']['wake_string']
WAKE_TIMER = int(config['WAKE']['wake_timer'])
SIM_NAME = int(config['DICT']['sim_name'])
SIM_LOCATION = int(config['DICT']['sim_location'])
SIM_ACTION = int(config['DICT']['sim_action'])
SOUND_WAKE = config['SOUNDS']['sound_wake']
SOUND_COMMAND_END = config['SOUNDS']['sound_command_end']

# Словарь для фразы активации
wake_alias = (WAKE_STRING,)

# Определяем класс Device
class Device:
    def __init__(self, main_topic, name, location, commands, status, sending):
        self.main_topic = main_topic
        self.name = name
        self.location = location
        self.commands = commands
        self.status = status
        self.sending = sending

devices = {
    "1": Device(
        main_topic='zigbee2mqtt/tv',
        name='телевизор',
        location='зал',
        commands={
            'status': 'stat',
            'sending': 'set',
            '/on_off/': {
                'включи, вруби, задействуй': 'on',
                'выключи, выруби, грохни': 'off'
            },
            '/volume/': {
                'громче': '+1',
                'тише': '-1',
                'звук': '5'
            },
            '/channel/': {
                'следующий': '+1',
                'предыдущий': '-1',
                'канал': '4'
            },
            '/mute/': {
                'включи': 'on',
                'выключи': 'off'
            }
        },
        status='stat',  # Добавьте статус
        sending='set'   # Добавьте отправку
    ),
    "2": Device(
        main_topic='input/light',
        name='свет',
        location='кухня',
        commands={
            'status': 'stat',
            'sending': 'set',
            '/on_off/': {
                'включи, вруби': 'on',
                'выключи, выруби': 'off'
            },
            '/brightness/': {
                'ярче': '+1',
                'темнее': '-1',
                'яркость': '3'
            },
            '/mode/': {
                'следующий': '+1',
                'предыдущий': '-1',
                'mode': '7'
            }
        },
        status='stat',  # Добавьте статус
        sending='set'   # Добавьте отправку
    )
}
# Инициализация клиента MQTT
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def subscribe_to_status_topics():
    for device_info in devices.values():
        for command_key in device_info.commands.keys():
            status_topic = f"{device_info.main_topic}{command_key}{device_info.status}"
            mqtt_client.subscribe(status_topic)
            print(f"Подписались на статус топик: {status_topic}")


def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')

    print(f"Получено сообщение на топик {topic}: {payload}")

mqtt_client.on_message = on_message
subscribe_to_status_topics()

def parse_command(command):
    action = None
    device_name = None
    location = None
    full_topic = None  # Здесь будем хранить полный топик

    # Проходим по всем устройствам для определения подходящих
    for device_key, device_info in devices.items():
        # Используем fuzz для сравнения
        score_name = fuzz.partial_ratio(device_info.name.lower(), command.lower())
        score_location = fuzz.partial_ratio(device_info.location.lower(), command.lower())

        # Проверяем, соответствуют ли значения порогам
        if score_name > SIM_NAME and score_location > SIM_LOCATION:
            device_name = device_info.name
            location = device_info.location
            print(f"Найдено устройство: {device_name} в {location} (score_name: {score_name}, score_location: {score>

            # Проверяем команды
            for command_key, command_options in device_info.commands.items():
                if isinstance(command_options, dict):
                    for synonyms, action_value in command_options.items():
                        for synonym in synonyms.split(','):
                            synonym = synonym.strip()  # Обрезаем пробелы
                            if synonym in command.lower():
                                score_action = fuzz.partial_ratio(synonym, command.lower())
                                if score_action > SIM_ACTION:
                                    action = action_value  # Устанавливаем действие
                                    full_topic = f"{device_info.main_topic}{command_key}{device_info.sending}"  # По>
                                    print(f"command_key: {command_key}, score_action: {score_action}")
                                    return device_name, location, full_topic, action

    return device_name, location, full_topic, action

def send_command(device_name, location, full_topic, action):
    if device_name and location and full_topic and action:
        print(f"Топик: {full_topic}")
        mqtt_client.publish(full_topic, action)
        print(f"Отправлена команда: {action} на {device_name} в {location}.")

def process_command(command):
    print("Команда: " + command)
    device_name, location, full_topic, action = parse_command(command)
    if device_name and location and action and full_topic:
        send_command(device_name, location, full_topic, action)
    else:
        print("Некорректный ввод. Попробуйте снова.")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def play_sound(file_path):
    data, samplerate = sf.read(file_path, dtype='float32')
    sd.play(data, samplerate)

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def reset_command_mode():
    global command_mode
    command_mode = False
    play_sound(SOUND_COMMAND_END)
    print("Режим команды отключен.")

def voice_listener():
    global command_mode
    command_mode = False  # Начинаем в режиме ожидания команды
    with sd.RawInputStream(callback=q_callback, channels=1, samplerate=samplerate, device=device_m, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)
        print("Начало прослушивания...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Распознанная фраза: {res}")
                    if any(alias in res for alias in wake_alias):
                        play_sound(SOUND_WAKE)  # Воспроизводим сигнал
                        command_mode = True
                        print("Фраза активации обнаружена. Теперь ожидаем команду...")
                        # Устанавливаем таймер на отключение режима команды
                        threading.Timer(WAKE_TIMER, reset_command_mode).start()
                    elif command_mode:
                        process_command(res)  # Обрабатываем команду только в режиме команд

if __name__ == "__main__":
    mqtt_client.connect(IP, int(PORT), 60)
    mqtt_client.loop_start()

    try:
        voice_listener()  # Начинаем прослушивание
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        mqtt_client.loop_stop()  # Останавливаем цикл обработки сообщений
        mqtt_client.disconnect()  # Разрывает соединение
