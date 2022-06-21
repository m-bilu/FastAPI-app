from pydantic import BaseSettings

# For setting up environment vars/file for constants
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


# Instance of settings class
settings = Settings()