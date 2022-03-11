
from django.http import HttpResponseRedirect

def my_login(func):
    def inner(*args, **kwargs):
        username = args[0].session.get('username')
        if username:
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    return inner

