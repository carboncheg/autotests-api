import grpc

import user_service_pb2
import user_service_pb2_grpc

# Устанавливаем соединение с сервером
channel = grpc.insecure_channel('localhost:50051')
stub = user_service_pb2_grpc.UserServiceStub(channel)

# Отправляем запрос
response = stub.GetUser(user_service_pb2.GetUserRequest(
    name="Alice",
    surname="Smith",
    age=20,
    gender="female",
    isMarried=False
))
print(response.greeting)  # Выведет: Привет, Alice!
print(response.dossier)
