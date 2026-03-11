from fastapi import APIRouter
from app.models.schemas import EmailRequest
from app.services.email_service import store_emails

router = APIRouter()

@router.get('/')
def check_root():
    return {"message" : "Working just fine!!"}


@router.post('/store-emails')
def emails_status(data : EmailRequest):
    data = store_emails(data)
    print(data)
    return {
        "success" : True,
        "data" : data
    }
