from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home(request: Request):
    accept = request.headers.get("Accept")
    if accept != "text/plain":
        return JSONResponse(content={"message": "Cannot accept other than plain text"}, status_code = 400)
    return JSONResponse(content={"message": "Welcome to this boilerplate"}, status_code = 200)
