from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from database import engine
from sqlalchemy import select, insert, delete, update
from models import TaskModel
from schemas import TaskCreateSchemas

tasks_router = APIRouter(prefix="/api/v1/tasks")

"""
    file = open('data.txt')
    file.write()
"""

@tasks_router.get(path='/list/')
def list_task_point(request: Request):
    session = Session(engine)
    stmt = select(TaskModel)
    """
    SELECT task.id, task.title, task.description, task.done 
    FROM task <- ссырой SQL запрос
    """
    requst_db = session.execute(stmt)
    tasks:list = requst_db.scalars().all()
    session.close()
    if len(tasks) == 0:
        return {"message": "У вас нет задач"}
    else:
        return {"message": tasks}


@tasks_router.post(path='/create/')
def create_task_point(request: Request, task: TaskCreateSchemas):
    session = Session(engine)
    stmt = insert(TaskModel).values(title=task.title,
                                    description=task.description)
    session.execute(stmt)
    session.commit()
    session.close()
    return task


@tasks_router.delete(path='/delete/{task_id}')
def delete_task_point(request: Request, task_id: int):
    session = Session(engine)
    stmt = delete(TaskModel).where(TaskModel.id == task_id)
    result = session.execute(stmt)
    session.commit()
    session.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    else:
        return {"message": "Задача успешно удалена"}
    


@tasks_router.put(path='/update/{task_id}')
def update_task_point(request: Request, task_id: int, task: TaskCreateSchemas):
    session = Session(engine)
    stmt = update(TaskModel).where(TaskModel.id == task_id).values(title=task.title, description=task.description)
    result = session.execute(stmt)
    session.commit()
    session.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    else:
        return {"message": "Задача успешно обновлена"}
