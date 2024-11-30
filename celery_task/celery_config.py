from settings import CELERY_URL

broker_url = CELERY_URL
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Moscow'
enable_utc = True