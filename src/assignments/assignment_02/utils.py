import json
from pydantic import BaseModel


class User_Info(BaseModel):
    first_name: str
    last_name:str
    email:str
    primary_coach_email:str
    secondary_coach_email:int
    account_id:int


class BsModel(BaseModel):
    name:str
    url:str
    bucket:str

def process_bsModel(bs_Model:BsModel):
    bs_data={
        "name":bs_Model.name,
        "url":bs_Model.url,
        "bucket":bs_Model.bucket
    }
    return bs_data


def process_user_data(user_create: User_Info):
    
    processed_user_data={
        "username":user_create.first_name+" "+user_create.last_name,
        "firstName":user_create.first_name,
        "lastName":user_create.last_name,
        "email":user_create.email,
        "secondary_email":user_create.primary_coach_email,
        "account_id":user_create.account_id
    }
    return processed_user_data



def custom_response(data):
    return {
        "success":True,
        "status_code":200,
        "data":data
    }



def get_modified_data(data,bsModel):

    existing_data = json.loads(data.settings_json)

    existing_data.update(bsModel)

    data.settings_json = json.dumps(existing_data)
    
    new_data={
        "brand_id":data.brand_id,
        "settings_json":data.settings_json,
        "inactive_settings": 0,
        "created_time": "2024-02-01T16:49:51",
        "created_by": 20105,
    }
    return new_data


