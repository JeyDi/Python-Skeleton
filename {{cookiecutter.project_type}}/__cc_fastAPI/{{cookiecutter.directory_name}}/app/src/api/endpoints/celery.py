import datetime as dt
from typing import Optional
from fastapi import APIRouter, Body, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from celery.result import AsyncResult


from app.src import models
from app.src.api import crud
from app.celery.task import worker
from app.src.common.utils import send_ping, profiling_api
from app.src.common.utils import write_log

#
router = APIRouter()
# define and inherit the base model for the CRUD operations over products
product = crud.base(models.Product)


def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@router.get("/test/{word}")
async def test_celery(word: str):
    '''
    Verify if Celery is working correctly
    @param {str} word - str
    @returns The task id.
    '''
    start_date = dt.datetime.now()
    task_result = worker.test_celery.delay(word)
    profiling_api("task:get:status", start_date, "info")
    return JSONResponse(task_result.id)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def run_task(
    payload=Body(
        ...,
        example={
            "name": "Test task",
            "time": 1,
        },
    )
):
    """
    Create a celery new task, remember to set the "time" field with a number
    """
    start_date = dt.datetime.now()
    timing = payload["time"]
    task_result = worker.create_task.delay(int(timing))
    profiling_api("task:create", start_date, "info")
    return JSONResponse({"task_id": task_result.id})


@router.get("/tasks/{task_id}")
async def get_status(task_id):
    """
    Get a status of a Celery task based on the task_id
    """
    start_date = dt.datetime.now()
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    profiling_api("task:get:status", start_date, "info")
    return JSONResponse(result)


# api example with background task
@router.get("/background")
async def ping(background_tasks: BackgroundTasks, message: str):
    start_date = dt.datetime.now()
    result = background_tasks.add_task(send_ping, "email@address.com", "Hi!")
    profiling_api("task:background", start_date, "info")
    return {"message": result}


@router.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
