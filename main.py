from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import get_current_user, get_current_user_with_refresh_token, create_tokens, authenticate
import models
import uvicorn

app = FastAPI()


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    class Config:
        orm_mode = True

class Contest(BaseModel):
    id: int
    class Config:
        orm_mode = True

class UserIn(BaseModel):
    name: str
    password: str

@app.post("/token", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)


@app.get("/refresh_token/", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user

@app.get("/contests/")
async def read_contests():
    ret = models.Contest.select()
    return [r for r in ret]

# 単一のTodoを取得
@app.get("/users/{user_id}")
def read_todo(user_id: int):
    return models.User.get_by_id(user_id)

# Todoを登録
@app.post("/users/")
async def create_todo(user_in: UserIn):
    user = models.User.create(name=user_in.name,password= user_in.password,is_admin = False)
    auth = authenticate(user.name, user.password)
    ret_dict = {}
    ret_dict["name"] = user.name
    ret_dict["tokens"] = create_tokens(user.id)
    return ret_dict

@app.get("/users/")
def read_todos():
    ret = models.User.select()
    return [r for r in ret]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)