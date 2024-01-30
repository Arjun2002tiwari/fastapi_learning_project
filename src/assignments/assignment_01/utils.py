import json
from sqlalchemy.orm import Session
from src.models import BrandSettings,Story,Brand



def get_inactive_settings(user_id:int,brand_id:int,db:Session):
    settings_json_results = db.query(BrandSettings.settings_json).filter(BrandSettings.id == user_id,
        BrandSettings.brand_id == brand_id,
        BrandSettings.inactive_settings == 0).first()

    return settings_json_results


def get_story_by_id(owner_id:int,story_id:int,db:Session):
    story_results=db.query(Story.title).filter(Story.id==story_id,Story.owner_id==owner_id).first()

    return story_results


def add_Brand(user_id:int,brand:dict,db:Session):
    brand["created_by"]=user_id
    brand["updated_by"]=user_id
    new_brand = Brand(**brand)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return {"success":True}


def update_brand_setting(user_id:int,brand_id:int,rec:dict,db:Session):
    record=db.query(BrandSettings).filter(BrandSettings.id == user_id,
        BrandSettings.brand_id == brand_id).first()
    if record:
        existing_data = json.loads(record.settings_json)

        # Update fields from the request
        existing_data.update(rec)

        # Update the "settings_json" field in the database
        record.settings_json = json.dumps(existing_data)

        # Commit the changes to the database
        db.commit()
        return record
    
def delete_record(user_id:int,req:dict,db:Session):
    db.query(Story).filter(Story.owner_id == user_id, Story.id == req["story_id"]).delete()
    db.commit()
    return {"success":True}
