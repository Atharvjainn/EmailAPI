from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def check_root():
    return {"message" : "Working just fine!!"}