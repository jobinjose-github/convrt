from fastapi import FastAPI
import uvicorn
from mangum import Mangum
from middlewares.user_verify_middleware import VerifyUserMiddleware
from routes.convrt_router import router as convrt_router
from routes.auth_router import router as auth_router
from services.auth_service import AuthService

app = FastAPI()

app.add_middleware(
    VerifyUserMiddleware,
    auth_service=AuthService(),
    exclude_paths=["/api/auth/login", "/api/auth/signup"],
)

app.include_router(convrt_router, prefix="/api/convrt")
app.include_router(auth_router, prefix="/api/auth")

@app.get("/")
def main():
    return "Welcome to Convrt API!"

handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)