import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Team, Project, Task, Comment

# Підключення до БД
engine = create_engine('sqlite:///app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def load_data(model, filename):
    with open(f'docs/demo/seed_data/{filename}') as f:
        data = json.load(f)
        for item in data:
            session.add(model(**item))
    session.commit()

# Завантаження даних
load_data(User, 'users.json')
load_data(Team, 'teams.json')
# Додаткові завантаження...

print("Database seeded successfully!")