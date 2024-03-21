from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from pydantic import BaseModel

app = FastAPI() # <- создаем экземпляр класса
app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

URLS = [
    {"tasks_post" : "127.0.0.1:8000/tasks/"}
]

class DatabaseJson:
    def __init__(self, name_db) -> None:
        self.__name_db = name_db

    def name_db(self):
        return self.__name_db

    def read(self) -> dict:
        with open(self.__name_db, 'r', encoding='utf-8') as db:
            return json.load(db)
    
    def write(self, data) -> None:
        with open(self.__name_db, 'w', encoding='utf-8') as db:
            json.dump(data, db, ensure_ascii=False, indent=4)

database = DatabaseJson('database.json')


class Task(BaseModel):
    """
    Схема обьекта, которую мы ожидаем получить от клиента
    """
    title:str
    description:str


class Users:
    def __init__(self, db):
        self.db = db
        self.users = []
        self.id = 1
        self.load_users()

    def load_users(self):
        data = self.db.read()
        users_data = data.get('users', [])
        self.users = [User(**user_data) for user_data in users_data]
        self.id = max(user.id for user in self.users) + 1

    def save_users(self):
        users_data = [user.__dict__ for user in self.users]
        data = {'users': users_data}
        self.db.write(data)

    def add_user(self, first_name, last_name):
        user = User(id=self.id, first_name=first_name, last_name=last_name)
        self.users.append(user)
        self.id += 1
        self.save_users()
        return user

    def get_users(self):
        return self.users

class User:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

users = Users(database)


@app.post('/tasks/')
def create_task(task:Task):
    task_data = {"title": task.title,"description": task.description}
    tasks = database.read()
    tasks['tasks'].append(task_data)
    database.write(tasks)


@app.get('/tasks/')
def get_tasks(request:Request):
    tasks = database.read()
    return templates.TemplateResponse(request=request, name='tasks.html', context={'tasks': tasks['tasks']})


@app.get('/users/', response_class=HTMLResponse)
def get_users(request: Request):
    users_list = users.get_users()
    return templates.TemplateResponse("users.html", {"request": request, "users": users_list})

@app.post('/users/')
def create_user(request: Request, first_name: str = Form(...), last_name: str = Form(...)):
    user = users.add_user(first_name, last_name)
    users_list = users.get_users()
    return templates.TemplateResponse("users.html", {"request": request, "users": users_list})





if __name__ == '__main__':
    print('Starting server')
    uvicorn.run('main:app', port=8000, reload=True)
    print('Server stopped')

# ls - комадна показывающая в консоле папки и файлы
# cd app - что бы перейти в директорию app
# cd .. - что бы вернуться на один уровень назад
# uvicorn main:app --reload