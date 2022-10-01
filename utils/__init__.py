from functools import partial, wraps

from pydantic import BaseModel


class ResponseModel(BaseModel):
    message: str
    status: bool = True
    alert: bool = False

    def reset(self):
        self.message = ""
        self.alert = False
        self.status = True

    def set(self, **kwargs):
        [setattr(self, key, value) for key, value in kwargs.items()]


def error_handler(func=None, error=None):
    if func is None:
        return partial(error_handler, error=error)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            err = error or "something went wrong"
            return ResponseModel(message=err, status=False)

    return wrapper


response = ResponseModel(message="")
