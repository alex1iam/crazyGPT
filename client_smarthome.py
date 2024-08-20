import paho.mqtt.client as mqtt
import socket
import json

# Функция для получения сообщения от сокет-сервера
def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))

    data = client_socket.recv(1024)
    result = json.loads(data.decode())
    print("Получено сообщение:", result["text"])
    client_socket.close()
    return result["text"]

# Создаем клиента для MQTT
mqtt_client = mqtt.Client()

# Обработчик подключения к MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

# Подключаем обработчик к MQTT клиенту
mqtt_client.on_connect = on_connect

# Подключаемся к брокеру
mqtt_client.connect(localhost, 1883, 60)

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

# Функция для отправки сообщения в MQTT
def send_mqtt_message(topic, message):
    mqtt_client.publish(topic, message)

# Функция для обработки команды
def process_command(command):
    # Базовые слова из команды
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

if __name__ == "__main__":
    # Подключаемся к MQTT брокеру и запускаем цикл обработки сообщений
#    mqtt_client.loop_start()


    # Получаем сообщение от сокет-сервера
    command = client()

    # Обрабатываем команду и отправляем её в MQTT
    process_command(command)

    # Останавливаем цикл обработки сообщений
#    mqtt_client.loop_stop()
    mqtt_client.loop_start()
