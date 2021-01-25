from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Python Redmine Grabber"
    redmine_api_token: str
    redmine_url: str

    class Config:
        env_file = ".env"