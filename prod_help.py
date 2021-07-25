def endless_try(func):
    def inner(*args, **kwargs):
        while(True):
            try:
                func(*args, **kwargs)
                print(f'{func.__name__} end')

            except Exception as e:
                print(e)
                print(f'{func.__name__} restart')

    return inner
