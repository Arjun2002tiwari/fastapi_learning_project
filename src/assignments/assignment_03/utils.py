from fastapi.responses import JSONResponse
from fastapi import status


def custom_exception_response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,message=None):
    '''return JSON response for exceptions.'''

    return JSONResponse(status_code=status,content={"message":message})



def custom_response(data=None):
    '''return modified response.'''

    return {
        "success":True,
        "status_code":status.HTTP_200_OK,
        "data":data
    }

