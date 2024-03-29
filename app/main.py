from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from database import engine, TaskModel
from routers import tasks_router
from urls import task_template

app = FastAPI() # <- создаем экземпляр класса
app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

app.include_router(tasks_router)
app.include_router(task_template)



if __name__ == '__main__':
    TaskModel.metadata.create_all(engine)
    print('Starting server')
    uvicorn.run('main:app', port=8000, reload=True)
    print('Server stopped')

