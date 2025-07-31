from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()

class Date(BaseModel):
    date: str
    hour: str

class PostModel(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: Date

all_posts: list[PostModel] = []

@app.get("/")
def home(request: Request):
    accept = request.headers.get("Accept")
    if accept != "text/plain":
        return JSONResponse(content={"message": "Cannot accept other than plain text"}, status_code = 400)
    return JSONResponse(content={"message": "Welcome to this boilerplate"}, status_code = 200)

@app.get("/ping")
def ping():
    return Response(content="pong", status_code=200, media_type="text/plain")

@app.get("/home")
def get_home():
    with open("./hello.html","r", encoding="utf-8") as file:
        file_html = file.read()
    return Response(content=file_html, status_code=200, media_type="text/html")


def serialized_stored_posts(posts: list[PostModel]):
    posts_converted = []
    for post in posts:
        posts_converted.append(post.model_dump())
    return posts_converted

@app.get("/posts")
def get_posts():
    serialized_posts = serialized_stored_posts(all_posts)
    return JSONResponse(
        content={
            "posts": serialized_posts
        },
        status_code=200
    )
@app.post("/posts")
def post(posts: list[PostModel]):
    for post in posts:
        all_posts.append(post)
    serialized_posts = serialized_stored_posts(posts);
    return serialized_posts

@app.get("/{full_path}")
def not_found():
    with open("./not-found.html", "r", encoding="utf-8") as file:
        file_html = file.read()
    return Response(content=file_html, status_code=404, media_type="text/html")
