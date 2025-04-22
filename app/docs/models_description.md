📊 Моделі даних та їх взаємозв'язки
1. User (Користувач)
python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    teams = relationship("Team", secondary=user_team, back_populates="members")

Атрибути:
id - унікальний ідентифікатор
username - унікальне ім'я користувача
email - унікальна електронна адреса
password - хеш пароля

Зв'язки:
Багато-до-багатьох з Team через таблицю user_team
Один-до-багатьох з Comment (користувач може мати багато коментарів)

2. Team (Команда)
python
class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    members = relationship("User", secondary=user_team, back_populates="teams")
    projects = relationship("Project", back_populates="team")

Атрибути:
id - унікальний ідентифікатор
name - назва команди
description - опис команди

Зв'язки:
Багато-до-багатьох з User через таблицю user_team
Один-до-багатьох з Project (команда може мати багато проектів)

3. Project (Проект)
python
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

Атрибути:
id - унікальний ідентифікатор
name - назва проекту
description - опис проекту
team_id - зовнішній ключ до команди

Зв'язки:
Багато-до-одного з Team (проект належить одній команді)
Один-до-багатьох з Task (проект може мати багато задач)

4. Task (Задача)
python
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(String(20), default="todo")
    priority = Column(String(20), default="medium")
    deadline = Column(DateTime)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")

Атрибути:
id - унікальний ідентифікатор
title - назва задачі
description - детальний опис
status - статус виконання (todo/in progress/done)
priority - пріоритет (low/medium/high)
deadline - крайній термін виконання
project_id - зовнішній ключ до проекту

Зв'язки:
Багато-до-одного з Project (задача належить одному проекту)
Один-до-багатьох з Comment (задача може мати багато коментарів)

5. Comment (Коментар)
python
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default='now()')
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="comments")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")

Атрибути:
id - унікальний ідентифікатор
text - текст коментаря
created_at - дата створення (автоматично встановлюється)
task_id - зовнішній ключ до задачі
user_id - зовнішній ключ до автора

Зв'язки:
Багато-до-одного з Task (коментар належить одній задачі)
Багато-до-одного з User (коментар має одного автора)

6. user_team (Асоціативна таблиця)
python
user_team = Table(
    'user_team',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('team_id', Integer, ForeignKey('teams.id'))
)
Призначення:
Реалізує зв'язок багато-до-багатьох між User і Team

🔗 Схема взаємозв'язків (у текстовому форматі)
User (1) ↔ (N) Team (1) ↔ (N) Project (1) ↔ (N) Task (1) ↔ (N) Comment
  ↑                                      ↑
  └──────────────────────────────────────┘
Ця структура дозволяє:
Користувачам бути в декількох командах
Командам мати багато проектів
Проектам містити багато задач
Задачам мати коментарі від різних користувачів