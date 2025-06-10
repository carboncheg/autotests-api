import socket
import threading
import time
import pytest


HOST = '127.0.0.1'
PORT = 12345


def tcp_server(stop_event):
    """Фоновый TCP-сервер, завершаемый через stop_event"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    server_socket.settimeout(0.1)

    while not stop_event.is_set():
        try:
            client_socket, _ = server_socket.accept()
            with client_socket:
                data = client_socket.recv(1024).decode()
                response = f'Сервер получил: {data}'
                client_socket.sendall(response.encode())
        except socket.timeout:
            continue
        except OSError:
            break

    server_socket.close()


@pytest.fixture(scope='module', autouse=True)
def server_thread():
    """Запуск сервера в фоне, остановка после тестов"""
    stop_event = threading.Event()
    thread = threading.Thread(target=tcp_server, args=(stop_event,))
    thread.start()
    time.sleep(0.2)  # Ждем старта сервера

    yield  # Выполняем тесты

    stop_event.set()

    # Пингуем сервер, чтобы accept() разблокировался
    try:
        with socket.create_connection((HOST, PORT), timeout=1) as s:
            s.sendall(b'stop')
    except Exception:
        pass

    thread.join(timeout=2)


@pytest.fixture
def send_message():
    """Фикстура клиента"""
    def _send(msg: str) -> str:
        with socket.create_connection((HOST, PORT), timeout=1) as sock:
            sock.sendall(msg.encode())
            sock.shutdown(socket.SHUT_WR)  # 💡 сигнал «данных больше не будет»
            return sock.recv(1024).decode()
    return _send


def test_hello(send_message):
    assert send_message('Привет') == 'Сервер получил: Привет'


def test_empty(send_message):
    assert send_message('') == 'Сервер получил: '


def test_long(send_message):
    msg = 'x' * 512
    assert send_message(msg) == f'Сервер получил: {msg}'
