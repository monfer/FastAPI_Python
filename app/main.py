from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine
from routers import post, user, auth, vote
from config import Settings
from fastapi.middleware.cors import CORSMiddleware



#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


try:
    conn = psycopg2.connect(host="localhost", database="FastAPIDb", user="postgres",
     password="Pass1234", cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successfull")
except Exception as error:
    print ("Connection to Database failed with error ")
    print ("Error: ", error)


my_posts = [{"title": "Title 1", "content":"content 1", "id":1}, 
            {"title": "Title 2", "content":"content 2", "id":2}]


def find_post(id):
    for post in my_posts:
        if post["id"]== int(id):
            return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}






