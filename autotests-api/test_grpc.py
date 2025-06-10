import grpc
import pytest
import time
from concurrent import futures

import user_service_pb2
import user_service_pb2_grpc
from grpc_server import UserServiceServicer  # импорт реализации сервиса


# Фикстура запускает сервер в отдельном потоке на время тестов
@pytest.fixture(scope='module')
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    port = server.add_insecure_port('localhost:0')  # выбирается свободный порт
    server.start()
    time.sleep(0.5)  # короткая пауза на запуск
    yield f'localhost:{port}'  # передача адреса клиента
    server.stop(None)


# Клиент gRPC, использующий адрес из grpc_server
@pytest.fixture
def grpc_stub(grpc_server):
    channel = grpc.insecure_channel(grpc_server)
    stub = user_service_pb2_grpc.UserServiceStub(channel)
    return stub


# ✅ Тест стандартного запроса
def test_get_user_success(grpc_stub):
    request = user_service_pb2.GetUserRequest(
        name='Alice',
        surname='Smith',
        age=20,
        gender='female',
        isMarried=False
    )
    response = grpc_stub.GetUser(request)

    assert response.greeting == 'Привет, Alice!'
    assert 'Alice' in response.dossier
    assert 'Smith' in response.dossier
    assert '20' in response.dossier
    assert 'female' in response.dossier
    assert 'IsMarried: False' in response.dossier


# ✅ Тест с пустыми строками и граничными значениями
def test_get_user_empty_fields(grpc_stub):
    request = user_service_pb2.GetUserRequest(
        name='',
        surname='',
        age=0,
        gender='',
        isMarried=True
    )
    response = grpc_stub.GetUser(request)

    assert response.greeting == 'Привет, !'
    assert 'Age: 0' in response.dossier
    assert 'IsMarried: True' in response.dossier


# ✅ Тест на передачу кириллицы
def test_get_user_cyrillic(grpc_stub):
    request = user_service_pb2.GetUserRequest(
        name='Андрей',
        surname='Иванов',
        age=30,
        gender='мужской',
        isMarried=True
    )
    response = grpc_stub.GetUser(request)

    assert response.greeting == 'Привет, Андрей!'
    assert 'Андрей' in response.dossier
    assert 'Иванов' in response.dossier
    assert '30' in response.dossier
    assert 'мужской' in response.dossier
