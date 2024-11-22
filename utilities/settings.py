from pydantic_settings import BaseSettings

# pydantic child class to manage environment variables
class EnvSetting(BaseSettings):
    db: str = "postgresql"
    db_name: str
    db_username: str = "postgres"
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432

    class Config:
        env_file = ".env"

# setting object to access env variables
setting = EnvSetting()