from fastapi import APIRouter, FastAPI
from src.assignments.assignment_01.assignment_01 import brand_router,story_router
app = FastAPI()

app.include_router(brand_router)
app.include_router(story_router)

@app.get('/')
def root_api():
    return {"message": "Welcome to CRUD App"}
