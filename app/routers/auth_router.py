from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.services.auth_service import login_user, register_user
from app.schemas.user import UserRegister, Token

router = APIRouter()

@router.post("/register")
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    access_token = login_user(db, form_data.username, form_data.password)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


###########################################################################################################################


#from fastapi import APIRouter, Depends
#from sqlalchemy.orm import Session
#from fastapi.security import OAuth2PasswordRequestForm

#from app.database import get_db
#from app.services.auth_service import login_user
#from app.schemas.user import Token

#router = APIRouter()

#@router.post("/login", response_model=Token)
#def login(
#    form_data: OAuth2PasswordRequestForm = Depends(),
#    db: Session = Depends(get_db)
#):
#    access_token = login_user(db, form_data.username, form_data.password)

#    return {
#        "access_token": access_token,
#        "token_type": "bearer"
#    }



###########################################################################################################################



#from fastapi import APIRouter, Depends, status
#from sqlalchemy.orm import Session

#from app.database import get_db
#from app.schemas.user import Token, UserLogin, UserRead, UserRegister
#from app.services.auth_service import login_user, register_user

#router = APIRouter(tags=["auth"])


#@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
#def register(payload: UserRegister, db: Session = Depends(get_db)):
#    return register_user(db, payload)


#@router.post("/login", response_model=Token)
#def login(payload: UserLogin, db: Session = Depends(get_db)):
#    access_token = login_user(db, payload.email, payload.password)
#    return Token(access_token=access_token)

