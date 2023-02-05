from functools import wraps
import traceback


def log_decorator():
    def wrap(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                return {'traceback': traceback.format_exc(), 'error': e.message}, 500

        return wrapped_function

    return wrap