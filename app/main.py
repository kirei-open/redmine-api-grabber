from functools import lru_cache
from fastapi import Depends, FastAPI
from redminelib import Redmine
from app import config
from fastapi.middleware.cors import CORSMiddleware


@lru_cache()
def get_settings():
    return config.Settings()


redmine = Redmine(get_settings().redmine_url, key=get_settings().redmine_api_token)

from .routers import admin, issues, projects, users

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(users.router, prefix="/users", tags=["users"])