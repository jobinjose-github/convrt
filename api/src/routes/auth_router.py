from fastapi import APIRouter
from models.request_model import SignUpModel, LoginModel
from services.auth_service import AuthService

router = APIRouter()

@router.post("/signup")
async def signup(user: SignUpModel):
    authService = AuthService()
    result = authService.signup(user)
    return result

@router.post("/login")
async def login(user: LoginModel):
    authService = AuthService()
    result = authService.login(user)
    return result