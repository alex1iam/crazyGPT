import paho.mqtt.client as mqtt
import sounddevice as sd
import vosk
import json
import queue

# Конфигурация
device_m = 1                                                  # Индекс аудиоустройства (микрофон)
model = vosk.Model("model_stt/vosk-model-small-ru-0.22")    # Модель нейросети
samplerate = 44100                                            # Частота дискретизации микрофона
q = queue.Queue()                                             # Потоковый контейнер

# Словари соответствий
equipment_dic = {
    "zigbee2mqtt/8acc. НИША Свет/set": ['свет в зале'],
    "zigbee2mqtt/jdy": ['лампа в кухне'],
    "zigbee2mqtt/5e24. КУХНЯ Лампа/set": ['пылесос']
}

action_dic = {
    "включи": ['on'],
    "открой": ['on', 'true', '1'],
    "выключи": ['off'],
    "закрой": ['off', 'false', '0'],
    "громче": ['+1'],
    "выше": ['+1'],
    "следующий": ['+1'],
    "тише": ['-1'],
    "ниже": ['-1'],
    "прежний": ['-1'],
    "предыдущий": ['-1']
}

# Создаем клиента для MQTT
mqtt_client = mqtt.Client()

# Обработчик подключения к MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

mqtt_client.on_connect = on_connect

# Функция для отправки сообщения в MQTT
def send_mqtt_message(topic, message):
    mqtt_client.publish(topic, message)

# Функция для обработки команды
def process_command(command):
    command_parts = command.lower().split()
    
    # Находим действие и устройство
    action = None
    equipment = None

    # Первое слово - это действие
    for part in command_parts:
        if part in action_dic:
            action = part
            break

    # Найти устройство
    for topic, names in equipment_dic.items():
        if any(name in command for name in names):
            equipment = topic
            break

    # Проверка, нашли ли действие и оборудование
    if action is None:
        print(f"Действие не распознано в команде '{command}'.")
        return

    if equipment is None:
        print(f"Устройство не найдено в команде '{command}'.")
        return

    # Получаем все сообщения, связанные с действием
    mqtt_message = ', '.join(action_dic[action])  # Объединяем все значения
    print(equipment, mqtt_message)

    # Если все найдено, отправляем сообщение
    send_mqtt_message(equipment, mqtt_message)
    print(f"Отправка '{mqtt_message}' в топик '{equipment}'")  # Тут производится отправка в MQTT сервер

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def voce_listen():
    with sd.RawInputStream(callback=q_callback, channels=1, samplerate=samplerate, device=device_m, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)
        print("Начало прослушивания...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Фраза целиком: {res}")
                    process_command(res)  # Обработка команды при распознавании
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")

if __name__ == "__main__":
    # Подключаемся к MQTT брокеру и запускаем цикл обработки сообщений
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()  # Запускаем цикл MQTT перед началом прослушивания

    try:
        voce_listen()  # Начинаем прослушивание
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        mqtt_client.loop_stop()  # Останавливаем цикл обработки сообщений