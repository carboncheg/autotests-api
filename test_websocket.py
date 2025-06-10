import pytest
import pytest_asyncio
import websockets


# Обработчик входящих сообщений
async def echo(websocket: websockets.ServerConnection):
    async for message in websocket:
        print(f'Получено сообщение: {message}')
        response = f'Сервер получил: {message}'
        await websocket.send(response)


# Асинхронная фикстура запуска WebSocket-сервера
@pytest_asyncio.fixture
async def websocket_server():
    server = await websockets.serve(echo, 'localhost', 0)
    port = server.sockets[0].getsockname()[1]
    uri = f'ws://localhost:{port}'

    yield uri

    server.close()
    await server.wait_closed()


# Тест подключения и ответа
@pytest.mark.asyncio
async def test_server_response(websocket_server):
    uri = websocket_server

    async with websockets.connect(uri) as websocket:
        test_message = 'Тестовое сообщение'
        await websocket.send(test_message)

        response = await websocket.recv()

        assert response == f'Сервер получил: {test_message}'
