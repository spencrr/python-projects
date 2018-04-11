import time
import labels

def timing(func):
    def wrapper(*args, **kwargs):
        import time
        s = time.time()
        func(*args, **kwargs)
        t = time.time() - s
        print('Ran ' + '''func.__name__''' + ' in {} sec'.format(t))
    return wrapper

@timing
def run():
    labels.main('Qualification Responses', 'Responses', 'Averages')

run()
