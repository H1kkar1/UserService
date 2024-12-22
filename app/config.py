from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pydantic import PostgresDsn


class RabbitSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 5672
    username: str
    password: str


class JWTSettings(BaseModel):
    secret: str
    algorithm: str
    access_token_expire_minutes: int


class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class RedisSettings(BaseModel):
    host: str = 'redis'
    port: int = 6379
    password: str = ''
    charset: str = ''
    decode_responses: bool = True
    db: int = 0


class RunSettings(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001
    reload: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    run: RunSettings = RunSettings()
    redis: RedisSettings = RedisSettings()
    db: DbSettings
    jwt: JWTSettings
    rmq: RabbitSettings


settings = Settings()
