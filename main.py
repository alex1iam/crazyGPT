import paho.mqtt.client as mqtt
import sounddevice as sd
import vosk
import json
import queue
import numpy as np
from fuzzywuzzy import fuzz
import soundfile as sf
import time
import threading
import configparser
from dict import dict_equipment, dict_action

# Конфигурация
device_m = 1
model = vosk.Model("model_stt/vosk-model-small-ru-0.22")
samplerate = 44100
q = queue.Queue()

# Чтение конфигураций
config = configparser.ConfigParser()
config.read('./settings.ini')

IP = config['MQTT']['ip']
PORT = config['MQTT']['port']
WAKE_STRING = config['WAKE']['wake_string']
WAKE_TIMER = config['WAKE']['wake_timer']
SIM_NAME = config['DICT']['sim_name']
SIM_LOCATION = config['DICT']['sim_location']
SIM_ACTION = config['DICT']['sim_action']
SOUND_WAKE = config['SOUNDS']['sound_wake']
SOUND_COMMAND_END = config['SOUNDS']['sound_command_end']

# Словарь для фразы активации
wake_alias = (WAKE_STRING,)

# Создаем клиента для MQTT
mqtt_client = mqtt.Client()

# Обработчик подключения к MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

mqtt_client.on_connect = on_connect

def send_mqtt_message(topic, message):
    mqtt_client.publish(topic, message)

def play_sound(file_path):
    data, samplerate = sf.read(file_path, dtype='float32')
    sd.play(data, samplerate)
#    sd.wait()  # Ждем, пока звук не закончится

def find_action(command):
    for part in command.split():
        for key in dict_action.keys():
            similarity = fuzz.ratio(part.lower(), key)
            if similarity > int(SIM_ACTION):
                return key
    return None

def find_equipment(command):
    command_lower = command.lower()
    for topic, details in dict_equipment.items():
        name_score = fuzz.partial_ratio(command_lower, details['name'].lower())
        location_score = fuzz.partial_ratio(command_lower, details['location'].lower())

        if name_score > int(SIM_NAME) and location_score > int(SIM_LOCATION):
            print(f"Найдено устройство: {details['name']} в {details['location']} (name_score: {name_score}, location_score: {location_s>
            return topic
    return None

def process_command(command):
    print(f"Обработка команды: '{command}'")
    action = find_action(command)
    equipment = find_equipment(command)

    if action is None:
        print(f"Действие не распознано в команде '{command}'.")
        return

    if equipment is None:
        print(f"Устройство не найдено в команде '{command}'.")
        return

    mqtt_message = ', '.join(dict_action[action])
    print(f"Найденное действие: {action}, Устройство: {equipment}, Отправка: {mqtt_message}")
    send_mqtt_message(equipment, mqtt_message)
    print(f"Отправка '{mqtt_message}' в топик '{equipment}'")

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
                    print(f"Фраза целиком: {res}")
                    if any(alias in res for alias in wake_alias):
                        play_sound(SOUND_WAKE)  # Воспроизводим сигнал
                        command_mode = True
                        print("Фраза активации обнаружена. Теперь ожидаем команду...")
                        # Устанавливаем таймер на отключение режима команды через 5 секунд
                        threading.Timer(int(WAKE_TIMER), reset_command_mode).start()
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
