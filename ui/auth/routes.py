# auth/routes.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas, models, auth

router = APIRouter()


@router.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate):
    """Sign up a new user."""
    if user.username in models.fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed = auth.hash_pasword(user.password)
    models.fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": hashed
    }
    return {"username": user.username}


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Log in a user and return an access token."""
    user = models.fake_users_db.get(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
