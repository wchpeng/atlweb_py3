import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atlweb_py3.settings")
app = Celery("atlweb_py3")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.config_from_object('django.conf:settings')
app.conf.broker_url = "redis://127.0.0.1:6379/4"
app.conf.result_backend = "redis://127.0.0.1:6379/4"
app.conf.accept_content = ["application/json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.timezone = "Asia/Shanghai"

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# add the periodic_task
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, test1.s("good -- every 10 seconds"), name="10s -- good")
#     sender.add_periodic_task(crontab(minute="*"), test1.s("=========================="), name="per minutes...")


@app.task(bind=True)
def test1(self, arg):
    print("{} his id is: {} --- {}".format(self.request.args, self.request.id, arg))