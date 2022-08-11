from flask import jsonify


def response(*args, **kwargs):
    """ 
    A template for creating api responses by jsonifying an optional list of arguments and an optional dictionary.
    """
    if (args):
        kwargs['args'] = args
    return jsonify(kwargs)

