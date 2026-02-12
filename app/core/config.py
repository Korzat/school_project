from pydantic_settings import BaseSettings, SettingsConfigDict


class MainSettings(BaseSettings):
    TOKEN_BOT: str
    API_KEY: str
    USER_DB: str
    PASSWORD_DB: str
    NAME_DB: str
    HOST_DB: str
    PORT_DB: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.USER_DB}:{self.PASSWORD_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = MainSettings()