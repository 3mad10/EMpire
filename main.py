from fastapi import FastAPI, Query, Request
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from smart_solutions.app.api.routes import solutions
from smart_solutions.app.api.routes import users
from smart_solutions.app.api.login import router as login_router
import uvicorn
from smart_solutions.app.api.deps import create_db_and_tables
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = FastAPI()
template = Jinja2Templates("templates")
template.env.auto_reload = True
template.env.loader = FileSystemLoader("templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/styles", StaticFiles(directory="templates/styles"), name= "styles")
app.mount("/images/main", StaticFiles(directory="resources/images/main"), name= "main-images")

app.include_router(solutions.router, prefix="/solutions")
app.include_router(users.router, prefix="/users")
app.include_router(login_router)

@app.get("/")
async def root(req : Request):
    return template.TemplateResponse(
        name="index.html",
        context={"request": req}
    )


smartApi = FastAPI()

@smartApi.get("/")
async def smart_root(req : Request):
    return template.TemplateResponse(
        name="smart-main.html",
        context={"request": req}
    )

smartApi.mount("/images/smart_solutions", StaticFiles(directory="resources/images/smart_solutions"), name="smart-solutions-images")
smartApi.mount("/videos/smart_solutions", StaticFiles(directory="resources/videos/smart_solutions"), name="smart-solutions-videos")
smartApi.mount("/svg/smart_solutions", StaticFiles(directory="resources/svg/smart_solutions"), name="smart-solutions-svg")
smartApi.mount("/static", StaticFiles(directory="templates/dynamic/smart_solutions"), name="static")
smartApi.mount("/styles", StaticFiles(directory="templates/styles"), name= "styles")
app.mount("/smart-solutions", smartApi)


# @app.on_event("startup")
# def on_startup():
#     try:
#         print("creating tables : ")
#         create_db_and_tables()
#     except Exception as e:
#         print(f"Error creating tables: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
