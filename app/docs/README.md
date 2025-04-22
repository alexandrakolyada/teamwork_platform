# Teamwork Platform

Це REST API-платформа для управління проєктами, користувачами та завданнями в команді. Розроблено з використанням FastAPI, SQLAlchemy та PostgreSQL. API дозволяє створювати проєкти, додавати завдання, призначати користувачів та відстежувати статус виконання.

## 📦 Основні можливості

- Створення та перегляд користувачів  
- Створення проєктів з датами початку і завершення  
- Призначення користувачів на проєкти  
- Створення завдань із дедлайнами, статусами та виконавцями  
- Валідація даних за допомогою Pydantic  
- Автоматичне створення документації Swagger UI  

## 🛠 Технології

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## 🚀 Як запустити проєкт локально

### 1. Клонуй репозиторій

```bash
git clone https://github.com/your-username/teamwork_platform.git
cd teamwork_platform
```

### 2. Створи віртуальне середовище

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Встанови залежності

```bash
pip install -r requirements.txt
```

### 4. Налаштуй змінні середовища

Створи файл `.env` і додай туди:

```
DATABASE_URL=postgresql://user:password@localhost:5432/your_database
```

(заміни `user`, `password`, `your_database` на свої значення)

### 5. Створи базу даних у PostgreSQL та застосуй міграції (за потреби)

### 6. Запусти сервер

```bash
uvicorn app.main:app --reload
```

### 7. Перевір API в браузері

```
http://127.0.0.1:8000/docs
```

## 📂 Структура проєкту

```
teamwork_platform/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── crud.py
│   ├── models
│   ├── schemas
│   ├── routes/
│   └── database.py
│
├── requirements.txt
└── README.md
```

## 📌 Примітки

🔸 У цій версії ролі користувачів ще не реалізовані. В майбутньому планується додати: `admin`, `manager`, `developer`.  
🔸 Проєкт орієнтований на вивчення створення REST API з FastAPI.  

 