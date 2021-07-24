from fastapi import Depends, FastAPI ,  File, UploadFile,Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from auth import get_current_user, get_current_user_with_refresh_token, create_tokens, authenticate
from starlette.middleware.cors import CORSMiddleware # 追加
import models
import uvicorn
import datetime
import shutil
from codeparty_simulator.exec import execute
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

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

def return_data(ret):
    return ret

@app.post("/token")
async def login(user_in: UserIn):
    """トークン発行"""
    user = authenticate(user_in.name, user_in.password)
    ret_dict = {}
    ret_dict["name"] = user.name
    ret_dict["tokens"] = create_tokens(user.id)
    return ret_dict


@app.get("/refresh_token/", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user_with_refresh_token)):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user


#Contest 関連

@app.get("/contests/{contest_id}")
def read_contests(contest_id: int):
    return models.Contest.get_by_id(contest_id).__data__ 

@app.get("/contests/")
async def read_contests():
    ret = models.Contest.select()
    return [r.__data__ for r in ret]


@app.post("/contests/")
async def create_contests(name:str,description:str):
    contest = models.Contest.create(name=name,discription=discription)
    return contest.__data__ 

@app.get("/contests/{contest_id}/codes")
def read_contest_codes(contest_id: int):
    ret = models.Code.select().where(models.Code.contest_id==contest_id)
    return [r.__data__ for r in ret]

@app.get("/contests/{contest_id}/rooms")
def read_contest_rooms(contest_id: int):
    ret =  models.Room.select().where(models.Room.contest_id==contest_id)
    return [r.__data__ for r in ret]

@app.get("/contests/{contest_id}/submitted")
def read_contest_submitted(contest_id: int,current_user:User = Depends(get_current_user)):
    ret =  models.Code.select().where(models.Code.contest_id==contest_id and models.Code.user_id==current_user.id)
    return [r.__data__ for r in ret]

#User 関連
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return models.User.get_by_id(user_id).__data__ 

@app.post("/users/")
async def create_user(user_in: UserIn):
    user = models.User.create(name=user_in.name,password= user_in.password,is_admin = False)
    auth = authenticate(user.name, user.password)
    ret_dict = {}
    ret_dict["name"] = user.name
    ret_dict["tokens"] = create_tokens(user.id)
    return ret_dict

@app.get("/users/")
def read_users():
    ret = models.User.select()
    return [r.__data__ for r in ret]


# Code 関連
@app.post("/codes/")
async def create_codes(contest_id:int, file: bytes = File(...),current_user:User = Depends(get_current_user)):
    print(current_user,contest_id,file)
    code = models.Code.create(user_id=current_user.id,contest_id= contest_id,time = datetime.datetime.now())

    with open("./static/submit/"+str(code.id)+".py", "wb") as buffer:
        shutil.copyfileobj(file, buffer)

    return code.__data__ 

@app.get("/codes/{code_id}")
async def read_code(code_id: int):
    return models.Code.get_by_id(code_id).__data__ 

@app.get("/codes/")
async def read_codes():
    ret = models.Code.select()
    return [r.__data__ for r in ret]

##Room 関連
@app.post("/rooms/", status_code=201)
async def create_room(contest_id:int,current_user:User = Depends(get_current_user)):
    room = models.Room.create(contest_id =contest_id)
    return room.__data__ 

@app.get("/rooms/{room_id}")
async def read_room(room_id: int):
    return models.Room.get_by_id(room_id).__data__ 

@app.get("/rooms/")
async def read_rooms():
    ret = models.Room.select()
    return [r.__data__ for r in ret]


@app.get("/rooms/{room_id}/run")
async def run_room(room_id: int):
    json = execute(["codeparty_simulator.players.sample2"]*4,room_id)
    return json

##Entry 関連
@app.post("/entries/", status_code=201)
async def create_entry(room_id:int,code_id:int):
    room = models.Entry.create(room_id = room_id)
    return room.__data__ 

@app.get("/entries/{entry_id}")
async def read_entry(entry_id: int):
    return models.Entry.get_by_id(entry_id).__data__ 

@app.get("/entries/")
async def read_entry():
    ret = models.Entry.select()
    return [r.__data__ for r in ret]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)