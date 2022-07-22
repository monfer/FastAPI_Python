from fastapi import HTTPException, APIRouter, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWSError, jwt
from requests import Session
from sqlalchemy.orm import session
from oauth2 import ALGORITHM, SECRET_KEY
import database, schemas, models, utilis, oauth2


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')

    if not utilis.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials')

    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token" : access_token, "token_type":"bearer"}




