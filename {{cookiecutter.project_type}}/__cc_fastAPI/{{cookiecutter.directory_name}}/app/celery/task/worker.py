import importlib
import time
from celery import Task

from app.celery.app import worker
from app.src.logger import logger

# from app.src.config import settings


class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """

    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logger.info("Loading Model...")
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
            logger.info("Model loaded")
        return self.run(*args, **kwargs)


@worker.task(
    ignore_result=False,
    bind=True,
    base=PredictTask,
    path=("celery_task_app.ml.model", "ChurnModel"),
    name="{}.{}".format(__name__, "Churn"),
)
def predict_churn_single(self, data):
    """
    Essentially the run method of PredictTask
    """
    pred_array = self.model.predict([data])
    positive_prob = pred_array[0][-1]
    return positive_prob


# task to verify if celery is working
@worker.task(name="test_celery", acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


# simple test task
@worker.task(name="create_task", acks_late=True)
def create_task(task_timing: int):
    time.sleep(int(task_timing) * 10)
    return True
