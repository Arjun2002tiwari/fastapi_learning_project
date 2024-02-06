import json
from fastapi import status
from sqlalchemy.orm import Session
from src.assignments.assignment_02.utils import custom_response
from src.assignments.assignment_03.schema import User_info
from src.assignments.assignment_03.utils import custom_exception_response
from src.models import Account, Brand, BrandSettings, BrandTelephonySetting, Language, User




def get_language_info(db:Session,user_id,account_id):

    try:
        
        query_results=db.query(Brand,BrandSettings)\
        .filter(User.id==user_id,Account.id==account_id)\
        .join(BrandSettings,BrandSettings.brand_id==Brand.id)\
        .join(Account,Account.brandName==Brand.id)\
            .join(User,User.account_id==Account.id).first()

        if not query_results:
            return custom_exception_response(status.HTTP_404_NOT_FOUND,"data not found!")
        
        # print(query_results.BrandSettings)
        setting_json = json.loads(query_results.BrandSettings.settings_json)
        
        query_res=db.query(Language).filter(Language.code==setting_json["preferred_language"]).first()

        if not query_res:
            return custom_exception_response(
                status.HTTP_404_NOT_FOUND,
                "data not found!")
        
        response_data={"Language_name":query_res.name,"brand_id":query_results.BrandSettings.brand_id,"multilingual_support":setting_json["multilingual_support"]}

        return custom_response(response_data)
    except Exception  as e:

        return custom_exception_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"something went wrong here! ,{e}"
        )
    




def get_ivrnumber(db:Session,user_id:int):

    try:
        query_Results=db.query(
            User.id.label("user_id"),
            Brand.id.label("brand_id"),
            Account.id.label("account_id"),
            BrandTelephonySetting.ivr_number.label("ivr_number"))\
            .filter(User.id==user_id,BrandTelephonySetting.brand_id==Brand.id)\
            .join(Brand,Brand.id==BrandTelephonySetting.brand_id)\
            .join(Account, Account.brandName==Brand.id)\
            .join(User, User.account_id==Account.id).first()
        
        if not query_Results:
            return custom_exception_response(
                status.HTTP_404_NOT_FOUND,
                "data not found!")

        return custom_response(query_Results)
    except Exception as e:
        
        return custom_exception_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"something went wrong here! ,{e}"
        )





def update_user(db:Session,body:dict,admin_user_id):
        
        try:
            model = User_info(**body)

            if (model.id)<0:
                return custom_exception_response(status.HTTP_400_BAD_REQUEST,"id is not positive integer!")
            
            users = db.query(User)\
                .filter(User.id.in_([model.id, admin_user_id])).all()
            
            if not users:
                return custom_exception_response(status.HTTP_404_NOT_FOUND,"users not found!")

            for user in users:
                for field, value in model:
                    if field != "id":
                        setattr(user, field, value)

            db.commit()
            return custom_response("updated successfully!")
        
        except Exception as e:
            return custom_exception_response(status.HTTP_422_UNPROCESSABLE_ENTITY,
                f"something went wrong here! ,{e}")
