# auth/routes.py
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from . import schemas, models, auth
from datetime import timedelta
from auth.dependencies import get_current_user

router = APIRouter()

@router.post("/signup", response_model=schemas.User)
async def signup(user: schemas.UserCreate, response: Response):
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
    
    # Automatically log in the user after signup
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    
    return {"username": user.username}

@router.post("/login", response_model=schemas.Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Log in a user and return an access token."""
    user = models.fake_users_db.get(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Set the token as an HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response):
    """Log out the current user."""
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}


@router.get("/me")
async def get_me(user: schemas.User = Depends(get_current_user)):
    """Get the current logged-in user."""
    return {"username": user.username}
