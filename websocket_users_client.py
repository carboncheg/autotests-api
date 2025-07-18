import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket:
        message = "Привет, сервер!"  # Сообщение, которое отправит клиент
        print(message)
        await websocket.send(message)  # Отправляем сообщение

        for _ in range(5):
            response = await websocket.recv()  # Получаем ответ от сервера
            print(response)


asyncio.run(client())
