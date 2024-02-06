from typing import Optional
from pydantic import BaseModel

class User_info(BaseModel):
    id:int
    username : str
    title : Optional[str] = None
    firstName : Optional[str] = None
    lastName : Optional[str] = None