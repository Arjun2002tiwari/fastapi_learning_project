from fastapi import APIRouter, Cookie, Depends
from src.assignments.assignment_01.utils import add_Brand, delete_record, get_inactive_settings, get_story_by_id, update_brand_setting
from sqlalchemy.orm import Session
from src.database import get_db

brand_router =APIRouter()
story_router=APIRouter()


#route to get setting_json.
@brand_router.get('/user/{user_id}/brand')
def get_setting_json(user_id:int,brand_id:int,session:Session=Depends(get_db)):
    data={"success":True,"user_id":user_id,"brand_id":brand_id}
    setting_json=get_inactive_settings(user_id,brand_id,session)
    data.update(setting_json)
    return data



#route to get story title.
@story_router.get('/user/{user_id}/story')
def get_story_data(
    user_id: int,
    story_id: int,session:Session=Depends(get_db)):
    data={"success":True,"owner_id":user_id}
    story_title=get_story_by_id(user_id,story_id,session)
    data.update(story_title)
    return data



#route to post new brand.
@brand_router.post('/user/{user_id}/brand')
def add_brand(user_id:int,brand:dict,session:Session=Depends(get_db)):
    brand_update=add_Brand(user_id,brand,session)  
    return brand_update                               



#route to update brand_settings.
@brand_router.put('/user/{user_id}/brand/{brand_id}')
def update_brandSetting(user_id:int,brand_id:int,rec:dict,session:Session=Depends(get_db)):
    update_Result=update_brand_setting(user_id,brand_id,rec,session)
    return update_Result



#route to delete story.
@story_router.delete('/user/{user_id}/delete/story')
def delete_rec(user_id:int,rec:dict,session:Session=Depends(get_db)):
    delete_result=delete_record(user_id,rec,session)
    return delete_result