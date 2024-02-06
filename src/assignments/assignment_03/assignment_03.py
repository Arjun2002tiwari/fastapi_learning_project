from fastapi import APIRouter,Depends,Request,status
from sqlalchemy.orm import Session
from src.assignments.assignment_03.schema import User_info
from src.assignments.assignment_03.utils import custom_exception_response
from src.assignments.assignment_03.helper import get_ivrnumber, get_language_info, update_user
from src.database import get_db



a03_router=APIRouter()

@a03_router.get("/language_name")
def get_language(request:Request,session:Session=Depends(get_db)):
    '''retrive language_name,brand_id,multiligual_support from language & brandSettings table using user_id & account_id.'''

    try:
        
        user_id=request.cookies.get("user_id")
        account_id=request.cookies.get("account_id")

        if (user_id==None) or (account_id==None):
            return custom_exception_response(status.HTTP_400_BAD_REQUEST,"user_id or account_id is not found!")
        
        if(not user_id.isdigit()) or (not account_id.isdigit()):
            return custom_exception_response(status.HTTP_400_BAD_REQUEST,"user_id or account_id is not valid integer!")
        
        query_results=get_language_info(session,user_id,account_id)

        return query_results
        
    except Exception as e:

        return custom_exception_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"something went wrong! ,{e}")






@a03_router.get('/ivr_number')
def get_ivr_number(request:Request,session:Session=Depends(get_db)):
    '''retrive ivr_number from brand_telephony_settings table using brand_id.'''

    try:
        user_id=request.cookies.get("user_id")

        if user_id is None:
            return custom_exception_response(status.HTTP_400_BAD_REQUEST,"user_id not found!")
        
        
        if not user_id.isdigit():
            return custom_exception_response(status.HTTP_400_BAD_REQUEST,"user_id is not valid integer!")
        
        
        query_results=get_ivrnumber(session,user_id)
        
        if query_results is None:

            return custom_exception_response(
                status.HTTP_404_NOT_FOUND,
                "data not found")
        
        return query_results
    
    except Exception as e:
        
        return custom_exception_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"something went wrong! ,{e}")





@a03_router.put("/update_user")
def update_user_info(request:Request,session:Session=Depends(get_db),body:dict=User_info):
    '''update fields in the user table whose ids are given.'''

    try:

        admin_user_id=request.cookies.get("admin_user_id")

        if admin_user_id is None:
            return custom_exception_response(status.HTTP_400_BAD_REQUEST,"admin_user_id not found!")
        
        if not admin_user_id.isdigit():
            return custom_exception_response(status.HTTP_400_BAD_REQUEST,"admin_user_id is not valid integer!")
        
        query_results=update_user(session,body,admin_user_id)

        return query_results
    
    except Exception as e:
        return custom_exception_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"something went wrong! ,{e}")