from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from pydantic import ValidationError
from config.config_loader import load_config
from db.db_ops import DBOps
from models.request_model import SignUpModel, LoginModel
import jwt
from datetime import datetime, timedelta


class AuthService:
    def __init__(self):
        self.configs = load_config()
        self.db_ops = DBOps()
        self.collection = "users"
        self.secret_key = self.configs["security"]["secret_key"]
        self.algorithm = self.configs["security"]["algorithm"]
        self.expire_delta = self.configs["security"]["expire_delta"]
        self.pwd_context = CryptContext(schemes=[self.configs["security"]["pswd_encrypt_scheme"]], deprecated="auto")

    def generate_token(self, user_data, expire_delta=30, secret_key=""):
        expire = datetime.now() + timedelta(minutes=expire_delta)
        to_encode = user_data.copy()
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, secret_key, algorithm=self.algorithm)
        return token

    def construct_password_salt(self, email, password):
        salts = email.split("@")
        password = salts[0][:10] + password[:80] + salts[1][:10]
        return password

    def signup(self, credentials: SignUpModel):
        try:
            data = {"email": credentials.email}
            user = self.db_ops.get_one(self.collection, data)
            print(user)
            if not user:
                password = self.construct_password_salt(
                    credentials.email, credentials.password
                )
                credentials.password = self.pwd_context.hash(password)
                result = self.db_ops.insert_one(self.collection, credentials.__dict__)
                print(result)
                if result:
                    data.update({"sub": result})
                    token = self.generate_token(
                        user_data=data, secret_key=self.secret_key, expire_delta=self.expire_delta
                    )
                    return {
                        "status": "success",
                        "message": "Signup Successfull!!!",
                        "token": token,
                    }
                else:
                    return {"status": "failed", "message": "Signup Failed!!!"}
            else:
                if user.get("email", "") and user.get("password", ""):
                    login_creds = LoginModel(
                        email=credentials.email, password=credentials.password
                    )
                    login_response = self.login(login_creds)
                    if login_response["status"] == "success":
                        return {
                            "status": "success",
                            "message": "User already exist.\nLoggedIn the user",
                            "token": login_response["token"],
                        }
                return {"status": "failed", "message": "User already exist!!!"}
        except Exception as e:
            return {"status": "failed", "message": "Signup Failed!!!"}

    def login(self, credentials: LoginModel):
        try:
            data = {"email": credentials.email}
            user = self.db_ops.get_one(self.collection, data)
            if user:
                password = self.construct_password_salt(
                    credentials.email, credentials.password
                )
                verified = self.pwd_context.verify(password, user["password"])
                if verified:
                    data.update({"sub": user["_id"]})
                    token = self.generate_token(
                        user_data=data, secret_key=self.secret_key, expire_delta=self.expire_delta
                    )
                    return {
                        "status": "success",
                        "message": "Login Successfull!!!",
                        "token": token,
                    }
                else:
                    return {"status": "failed", "message": "Wrong password!!!"}
            else:
                return {"status": "failed", "message": "User account does not exist!!!"}
        except Exception as e:
            return {"status": "failed", "message": "Login Failed!!!"}

    def verify_user_token(self, token: str):
        try:
            user_data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if user_data and user_data.get("email", "") and user_data.get("sub"):
                return user_data
            else:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"status": "failed", "message": "Invalid or expired token"},
                )
        except jwt.PyJWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": "failed", "message": "Invalid or expired token"},
            )
