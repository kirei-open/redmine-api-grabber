from functools import lru_cache
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jose import JWTError, jwt

from redminelib import Redmine

from apscheduler.schedulers.background import BackgroundScheduler

import mysql.connector

from app import config


@lru_cache()
def get_settings():
    return config.Settings()


redmine = Redmine(get_settings().redmine_url, key=get_settings().redmine_api_token)

app = FastAPI(title="Redmine API Grabber", root_path="/api/v1")

db = mysql.connector.connect(
    host=get_settings().redmine_db_host,
    user=get_settings().redmine_db_user,
    password=get_settings().redmine_db_password,
    database=get_settings().redmine_db_name,
)

db_portal = mysql.connector.connect(
    host=get_settings().portal_db_host,
    user=get_settings().portal_db_user,
    password=get_settings().portal_db_password,
    database=get_settings().portal_db_name,
)

Schedule = None


from .routers import admin, issues, projects, users
from .services import scheduler
from app.dependencies import get_token_header


@app.on_event("startup")
async def load_schedule_or_create_blank():
    """
    Instatialise the Schedule Object as a Global Param and also load existing Schedules from SQLite
    This allows for persistent schedules across server restarts.
    """
    global Schedule
    try:
        Schedule = BackgroundScheduler()
        Schedule.add_job(
            scheduler.insert_issues_statuses, "cron", hour="*/1", id="issues"
        )
        Schedule.start()
        print("Created Schedule Object")
    except:
        print("Unable to Create Schedule Object")


@app.on_event("shutdown")
async def pickle_schedule():
    """
    An Attempt at Shutting down the schedule to avoid orphan jobs
    """
    global Schedule
    Schedule.shutdown()
    print("Disabled Schedule")


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