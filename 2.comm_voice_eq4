import paho.mqtt.client as mqtt
import sounddevice as sd
import vosk
import json
import queue
import numpy as np
from fuzzywuzzy import fuzz
import soundfile as sf
import time
import threading  # Импортируем библиотеку threading

# Конфигурация
device_m = 1
model = vosk.Model("model_stt/vosk-model-small-ru-0.22")
samplerate = 44100
q = queue.Queue()

# Словари соответствий
equipment_dic = {
    "input/light_z0_on_off": {'name': 'свет', 'location': 'милайт'},
    "input/light_z2_on_off": {'name': 'свет', 'location': 'зал'},
    "zigbee2mqtt/5e24. КУХНЯ Лампа/set": {'name': 'лампа', 'location': 'кухня'},
    "input/light_z3_on_off": {'name': 'люстра', 'location': 'зал'},
    "input/light_z4_on_off": {'name': 'свет', 'location': 'кухня'},
    "input/light_z1_on_off": {'name': 'свет', 'location': 'прихожая'},
    "zigbee2mqtt/9665. ВАННАЯ Свет/set": {'name': 'свет', 'location': 'ванная'},
    "zigbee2mqtt/8acc. НИША Свет/set": {'name': 'свет', 'location': 'ниша'},
    "zigbee2mqtt/cfa4. ЗАЛ Штора справа/set": {'name': 'штора справа', 'location': 'зал'},
    "zigbee2mqtt/d38e. ЗАЛ Штора в центре/set": {'name': 'штора центр', 'location': 'зал'},
    "zigbee2mqtt/8e8a. ЗАЛ Штора слева/set": {'name': 'штора слева', 'location': 'зал'},
    "zigbee2mqtt/29c6. КУХНЯ Штора справа/set": {'name': 'штора справа', 'location': 'кухня'},
    "zigbee2mqtt/4d83. КУХНЯ Штора слева/set": {'name': 'штора слева', 'location': 'кухня'},
    "zigbee2mqtt/639b. ВАННАЯ Клапан горячей воды/set": {'name': 'горячая вода', 'location': 'ванная'},
    "zigbee2mqtt/37cf. ВАННАЯ Клапан холодной воды/set": {'name': 'холодная вода', 'location': 'ванная'},
    "zigbee2mqtt/e4ee. ЗАЛ Умная розетка/set": {'name': 'розетка', 'location': 'зал'},
    "zigbee2mqtt/e945. ЗАЛ Теплый пол/set": {'name': 'пол', 'location': 'зал'}
}

action_dic = {
    "включи": ['on'],
    "открой": ['open'],
    "выключи": ['off'],
    "закрой": ['close'],
    "громче": ['+1'],
    "выше": ['+1'],
    "следующий": ['+1'],
    "тише": ['-1'],
    "ниже": ['-1'],
    "прежний": ['-1'],
    "предыдущий": ['-1']
}

# Словарь для фразы активации
sys_alias = ('альфа',)

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
    sd.wait()  # Ждем, пока звук не закончится

def find_action(command):
    for part in command.split():
        for key in action_dic.keys():
            similarity = fuzz.ratio(part.lower(), key)
            if similarity > 95:
                return key
    return None

def find_equipment(command):
    command_lower = command.lower()
    for topic, details in equipment_dic.items():
        name_score = fuzz.partial_ratio(command_lower, details['name'].lower())
        location_score = fuzz.partial_ratio(command_lower, details['location'].lower())

        if name_score > 70 and location_score > 70:
            print(f"Найдено устройство: {details['name']} в {details['location']} (name_score: {name_score}, location_score: {location_score})")
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

    mqtt_message = ', '.join(action_dic[action])
    print(f"Найденное действие: {action}, Устройство: {equipment}, Отправка: {mqtt_message}")
    send_mqtt_message(equipment, mqtt_message)
    print(f"Отправка '{mqtt_message}' в топик '{equipment}'")

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def reset_command_mode():
    global command_mode
    command_mode = False
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
                    if any(alias in res for alias in sys_alias):
                        play_sound('alpha.wav')  # Воспроизводим сигнал
                        command_mode = True
                        print("Фраза активации обнаружена. Теперь ожидаем команду...")
                        # Устанавливаем таймер на отключение режима команды через 5 секунд
                        threading.Timer(5.0, reset_command_mode).start()
                    elif command_mode:
                        process_command(res)  # Обрабатываем команду только в режиме команд

if __name__ == "__main__":
    mqtt_client.connect('192.168.200.204', 1883, 60)
    mqtt_client.loop_start()

    try:
        voice_listener()  # Начинаем прослушивание
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        mqtt_client.loop_stop()  # Останавливаем цикл обработки сообщений
