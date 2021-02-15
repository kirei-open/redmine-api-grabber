from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Python Redmine Grabber"
    redmine_api_token: str
    redmine_url: str
    redmine_db_host: str
    redmine_db_name: str
    redmine_db_user: str
    redmine_db_password: str
    portal_db_host: str
    portal_db_name: str
    portal_db_user: str
    portal_db_password: str

    class Config:
        env_file = ".env"