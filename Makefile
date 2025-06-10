# Указание путей
PROTO_SRC=user_service.proto
GEN_DIR=.

# Команда генерации gRPC-кода из .proto
generate:
	@echo "🔧 Генерация gRPC-классов из $(PROTO_SRC)..."
	python -m grpc_tools.protoc \
		-I. \
		--python_out=$(GEN_DIR) \
		--grpc_python_out=$(GEN_DIR) \
		$(PROTO_SRC)
	@echo "✅ Готово: user_service_pb2*.py"

# Запуск локального сервера
run-server:
	@echo "🚀 Запуск gRPC-сервера..."
	python $(GEN_DIR)/grpc_server.py

# Отправка запроса от клиента
request:
	@echo "📧 Отправка запроса от клиента..."
	python $(GEN_DIR)/grpc_client.py

# Очистка сгенерированных файлов
clean:
	@echo "🧹 Очистка сгенерированных файлов..."
	rm -f $(GEN_DIR)/user_service_pb2*.py

# Запуск автотестов
test:
	pytest -v $(GEN_DIR)/test_get_user.py

# Команда по умолчанию
.DEFAULT_GOAL := generate
