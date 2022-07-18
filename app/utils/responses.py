import logging

from fastapi.responses import JSONResponse


class CommonResponse(JSONResponse):
    """
    This is case of response ins common case.
    Don't use this response directly.
    """

    def __init__(self,
                 success: bool = True,
                 message: str = 'Success!',
                 status_code: int = 200,
                 **kwargs):
        self.param = {
            'success': success,
            'message': message
        }

        self.param.update(kwargs)
        logging.debug(f'CommonResponse param: {self.param}')

        super().__init__(content=self.param, status_code=status_code)


class SuccessResponse(CommonResponse):
    ...


class FailureResponse(CommonResponse):
    def __init__(self, status_code: int, success: bool = False, message: str = 'Success!', **kwargs):
        self.param = {
            'success': success,
            'message': message
        }
        self.param.update(kwargs)
        logging.debug(f'CommonResponse param: {self.param}')

        super().__init__(content=self.param, status_code=status_code)
