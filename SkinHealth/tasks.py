from celery import task


@task()
def test():
    while 1:
        print(123)
