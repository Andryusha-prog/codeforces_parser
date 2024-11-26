from celery import Celery

app = Celery('celery_task', include=['celery_task.tasks'])
app.config_from_object('celery_task.celery_config')
app.conf.beat_schedule = {
    'everyday-task': {
      'task': 'celery_task.tasks.update_data',
      'schedule': 30.0
    }
}
