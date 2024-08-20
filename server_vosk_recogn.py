import sounddevice as sd
import vosk
import json
import queue
import socket
import SOAPpy

def serve(conn):
    print('Сервер запущен. Ожидание подключения...')

    # Обработка запросов от клиента
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print("Получено сообщение:", data.decode())
        except Exception as e:
            print("Ошибка:", e)
            break

    conn.close()
    print("Соединение закрыто.")

# Визуальная переменная для сокета
device_m = 1                                                  # Индекс аудиоустройства (микрофон)
model = vosk.Model("model_stt/vosk-model-small-ru-0.22")      # Модель нейросети
samplerate = 44100                                            # Частота дискретизации микрофона
q = queue.Queue()                                             # Потоковый контейнер

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

def voce_listen(conn):
    with sd.RawInputStream(callback=q_callback, channels=1, samplerate=samplerate, device=device_m, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)
        print("Начало прослушивания...")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Фраза целиком: {res}")
                    # Отправляем распознанное сообщение через сокет
                    conn.sendall(json.dumps({"text": res}).encode())
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")


def run_soap_server():
    try:
        SOAPpy.Config.debug = 1
        server = SOAPpy.SOAPServer(("localhost", 8080))
        server.registerFunction(hello)  # Предполагается, что hello определено
        server.serve_forever()
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    # Создание и настройка сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)

    conn, addr = server_socket.accept()
    print('Подключен:', addr)

    # Запускаем сервер SOAP в отдельном потоке
    import threading
    soap_thread = threading.Thread(target=run_soap_server)
    soap_thread.start()

    # Запускаем распознавание речи
    try:
        voce_listen(conn)
    finally:
        # Убедитесь, что сокет закрыт перед выходом
        server_socket.close()
        print("Сервер остановлен.")