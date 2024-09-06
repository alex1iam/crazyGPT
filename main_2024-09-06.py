import paho.mqtt.client as mqtt
import telegram
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
from dict import Device, devices, groups

bot_token = '54999998983:AAFhouigyufuyfhjfjkjb6VyTf6wTxY4'  # Замените на свой токен
chat_id = '6464666642'  # Замените на свой ID чата
bot = telegram.Bot(token=bot_token)

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
SIM_WAKE = int(config['DICT']['sim_wake'])
SIM_NAME = int(config['DICT']['sim_name'])
SIM_LOCATION = int(config['DICT']['sim_location'])
SIM_ACTION = int(config['DICT']['sim_action'])
SOUND_WAKE = config['SOUNDS']['sound_wake']
SOUND_COMMAND_DONE = config['SOUNDS']['sound_command_done']
SOUND_COMMAND_END = config['SOUNDS']['sound_command_end']

# Словарь для фразы активации
wake_alias = (WAKE_STRING,)

prev_topic_value = None

action = None
device_name = None
location = None
full_topic = None

# Инициализация клиента MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(IP, int(PORT), 60)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_to_status_topics()  # Вызываем подписку на топики после подключения

def subscribe_to_status_topics():
    for device_info in devices.values():
        for command_key in device_info.commands.keys():
            # Добавляем разделитель между частями, чтобы избежать проблем с формированием топиков
            status_topic = f"{device_info.main_topic}{command_key}{device_info.status}"
            status_topic = status_topic.replace('//', '/')  # Замена двойных слешей на одинарные
            mqtt_client.subscribe(status_topic)
            print(f"Подписались на статус топик: {status_topic}")

def on_message(client, userdata, message):
    global prev_topic_value
    curr_topic_value = message.payload.decode("utf-8")  # Декодируем сообщение
    if prev_topic_value != curr_topic_value:
        bot.sendMessage(chat_id=chat_id, text=f"{message.topic}:: {curr_topic_value}")  # Исправлено на message.topic
        prev_topic_value = curr_topic_value
        print(f"Получено сообщение в топик {message.topic}: {curr_topic_value}")
        print(f"Отправлено сообщение в чат: команда '{action}' на '{device_name}' в '{location}'")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def parse_command(command):
    global action
    global device_name
    global location
    global full_topic

    # Проходим по всем устройствам для определения подходящих
    for device_key, device_info in devices.items():
        # Используем fuzz для сравнения
        score_name = fuzz.partial_ratio(device_info.name.lower(), command.lower())
        score_location = fuzz.partial_ratio(device_info.location.lower(), command.lower())

        # Проверяем, соответствуют ли значения порогам
        if score_name > SIM_NAME and score_location > SIM_LOCATION:
            device_name = device_info.name
            location = device_info.location
            print(f"Найдено устройство: {device_name} в {location} (score_name: {score_name}, score_location: {score_location})")

            # Проверяем команды
            for command_key, command_options in device_info.commands.items():
                if isinstance(command_options, dict):
                    for synonyms_tuple, action_value in command_options.items():
                        # Проверяем наличие любого синонима в команде
                        if any(synonym in command.lower() for synonym in synonyms_tuple):
                            action = action_value  # Устанавливаем действие
                            full_topic = f"{device_info.main_topic}{command_key}{device_info.sending}"  # Полный>
                            print(f"command_key: {command_key}")
                            return device_name, location, full_topic, action

    return device_name, location, full_topic, action

def send_command(device_name, location, full_topic, action):
    if device_name and location and full_topic and action:
        print(f"Топик: {full_topic}")
        mqtt_client.publish(full_topic, action)
        play_sound(SOUND_COMMAND_DONE)
        print(f"Отправлена команда: {action} на {device_name} в {location}.")

def process_command(command):
    print("Команда: " + command)
    device_name, location, full_topic, action = parse_command(command)
    if device_name and location and action and full_topic:
        send_command(device_name, location, full_topic, action)
    else:
        print("Некорректный ввод. Попробуйте снова.")

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
                    # Используем fuzzy для сравнения
                    score_wake = fuzz.partial_ratio(res, wake_alias)
                    print(f"score_wake: {score_wake}")
                    if score_wake > SIM_WAKE:
                        res = wake_alias
                        if any(alias in res for alias in wake_alias):
                            play_sound(SOUND_WAKE)  # Воспроизводим сигнал
                            command_mode = True
                            print("Фраза активации обнаружена. Теперь ожидаем команду...")
                            # Устанавливаем таймер на отключение режима команды
                            threading.Timer(WAKE_TIMER, reset_command_mode).start()
                    elif command_mode:
                        process_command(res)  # Обрабатываем команду только в режиме команд

if __name__ == "__main__":
    mqtt_client.loop_start()

    try:
        voice_listener()  # Начинаем прослушивание
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        mqtt_client.loop_stop()  # Останавливаем цикл обработки сообщений
        mqtt_client.disconnect()  # Разрывает соединение
