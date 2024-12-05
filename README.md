### File Storage
REST API для сохранения файла

Клонируйте проект себе на компьютер:
```bash
git clone https://github.com/zifrit/kanban.git
```
Активации виртуального окружения
```bash
poetry shell
```
Установка всех зависимостей
```bash
poetry install
```
Запуск 
```bash
poetry run python main.py 
```

#### Документация будет доступна по адресу http://0.0.0.0:8000/api/openapi

#### Endpoints

Загрузка файла
```bash
POST http://127.0.0.1:8000/api/files/upload
```

Загрузка большого файла через стрим
```bash
POST http://127.0.0.1:8000/api/files/upload?large=ture&chunk_size=1048576
```

Получение файла по его UID (UUID)
```bash
GET http://127.0.0.1:8000/api/files/{filed_id}
```
Получение списка файла загруженных файлов
```bash
GET http://127.0.0.1:8000/api/files/
```