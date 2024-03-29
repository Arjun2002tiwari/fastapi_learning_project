from fastapi import Cookie, Depends, FastAPI,Request
#from src.assignments.assignment_01.assignment_01 import brand_router,story_router
#from src.assignments.assignment_02.assignment_02 import a02_router
from src.assignments.assignment_03.assignment_03 import a03_router
app = FastAPI()

#app.include_router(brand_router,prefix="/assignment_01")
#app.include_router(story_router,prefix="/assignment_01")
#app.include_router(a02_router,prefix="/assignment_02")
app.include_router(a03_router,prefix="/assignment_03")

@app.get('/')
def root_api():
    return {"message": "Welcome to CRUD App"}
