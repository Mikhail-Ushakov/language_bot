from celery import Celery
import requests as r


app = Celery('celery', broker='redis://0.0.0.0:6379/0', backend='redis://0.0.0.0:6379/0')

app.conf.broker_connection_retry_on_startup = True
# app.conf.broker_url = 'redis://localhost:6379/0'
# app.conf.result_backend = 'redis://localhost:6379/0'
# app.conf.update(
#     result_expires=3600,
# )


# @app.task
# def hello():
#     response = r.get('https://thetldr.tech/content/images/2021/08/image-1.png').content
#     print('hello')
#     with open('test.png', 'wb') as f:
#         f.write(response)