from fastapi import APIRouter, Cookie,Depends
from src.assignments.assignment_02.utils import custom_response, get_modified_data, process_bsModel, process_user_data
from sqlalchemy.orm import Session
from src.models import Account, Brand, BrandSettings,User,Story
from src.database import get_db
from fastapi.responses import JSONResponse

a02_router=APIRouter()

#@a02_router.get("/{user_id}")
#async def tbl_join(
#    user_id: int,
#    account_id: int,
#    db: Session = Depends(get_db)
#):
#   query = db.query(Account.id.label("account_id"), Brand.id.label("brand_id"), Brand.name.label("brand_name")).filter(Account.id==account_id)\
#    .join(Brand, Brand.id==Account.brandName).first()
#    print(query.brand_name)
#    return {"1": "hi"}


#add user in the User table.
@a02_router.post('/add_user')
def add_user(user: dict = Depends(process_user_data),db:Session=Depends(get_db)):
    try:
        # new_user=User(**user)
        new_user=User(user.username,)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        query_results=db.query(
            User.id.label("user_id"),
            Account.id.label("account_id"), 
            Brand.id.label("brand_id"), 
            Brand.name.label("brand_name"))\
            .filter(User.id==new_user.id,Account.id==new_user.account_id)\
            .join(Brand,Brand.id==Account.brandName).first()

        if query_results:
            return custom_response(query_results)
        
        return JSONResponse(status_code=404,content={"message":"data not found!"})
    except:
        return JSONResponse(status_code=400,content={"something went wrong!"})





#update setting_json,inactive_Settings in brand_settings table.
@a02_router.post('/brand_setting')
def update_brand_setting(bsModel:dict=Depends(process_bsModel),loggedIn_id:int=Cookie(),db:Session=Depends(get_db)):
    try:
        query_results = (
        db.query(User,BrandSettings)
        .filter(User.id == loggedIn_id, BrandSettings.inactive_settings == 0)
        .join(Account, User.account_id == Account.id)
        .join(Brand, Account.brandName == Brand.id)
        .join(BrandSettings, Brand.id == BrandSettings.brand_id)
        .first()
        )
        
        db.query(BrandSettings).filter(BrandSettings.id==query_results.BrandSettings.id).update({"inactive_settings": 1})

        new_brandSetting_data=get_modified_data(query_results.BrandSettings,bsModel)
        new_data=BrandSettings(**new_brandSetting_data)
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        print(new_data.settings_json)
        import json

        setting_json = json.loads(new_data.settings_json)
        print(setting_json)


        response_data={"user_id":loggedIn_id,"brand_id":new_data.brand_id,"brand_setting": setting_json}
        return {"success":True,"status_code":200,"data":response_data}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400,content={"message":"something went wrong!"})





#get all stories where inactive is 0 from Story table.
@a02_router.post('/get_story')
def get_story(user_id: int = Cookie(),db:Session=Depends(get_db)):
        try:
            query_results=db.query(
                User.id.label("user_id"),
                Account.id.label("account_id"), 
                Brand.id.label("brand_id"),
                Story.id,
                Story.title
            )\
            .filter(User.id==user_id,Story.inactive == 0)\
            .join(Brand, Story.brand_id == Brand.id)\
            .join(Account, Brand.id == Account.brandName)\
            .join(User, Account.id == User.account_id).all()

            if query_results:

                stories = []
                result_dict = {"user_id": user_id, "account_id": query_results[0].account_id, "brand_id": query_results[0].brand_id, "stories": stories}

                for row in query_results:
                   
                    s_dta = {"story_id": row.id, "story_title": row.title}
                    stories.append(s_dta)

                return custom_response(data=result_dict)
            
            return JSONResponse(status_code=404,content={"message":"data not found!"})
        
        except:
             return JSONResponse(status_code=400,content={"message":"something went wrong!"})
        




#change inactive status in the User table.
@a02_router.put('/update_status')
def update_status(user_ids:str=Cookie(),statuses:str=Cookie(),db:Session=Depends(get_db)):
    try:
        user_ids_list = [int(user_id) for user_id in user_ids.split(" ")]
        status_list=[int(status) for status in statuses.split(" ")]


        
        for user_id,inactive in zip(user_ids_list,status_list):
            db.query(User).filter(User.id == user_id ,User.inactive!=2).update({"inactive":inactive})
        db.commit()

        response_data = [
            {"user_id": user_id, "status": status} for user_id, status in zip(user_ids_list, status_list)
            ]
        return custom_response(response_data)
    except:
        return JSONResponse(status_code=400,content={"message":"something went wrong!"})
        
          