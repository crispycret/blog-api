from flask import jsonify

from core import app

from .utils import response



@app.route('/')
def index():
    args = ['arg1', 'arg2', 'arg3']
    kwargs = {'kwarg1':1, 'kwarg2':2, 'kwarg3':3}
    return response(*args, **kwargs)
    # return response('arg1', 'arg2', kwarg1=1)


