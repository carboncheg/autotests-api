import asyncio

import websockets


# Обработчик входящих сообщений
async def echo(websocket: websockets.ServerConnection):
    async for message in websocket:
        print(f"Получено сообщение: {message}")
        response = f"Сервер получил: {message}"
        await websocket.send(response)  # Отправляем ответ


# Запуск WebSocket-сервера на порту 8765
async def main():
    server = await websockets.serve(echo, "localhost", 8765)
    print("WebSocket сервер запущен на ws://localhost:8765")
    await server.wait_closed()


asyncio.run(main())
