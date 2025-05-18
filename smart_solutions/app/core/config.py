from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl
from pydantic import (
    HttpUrl,
    MySQLDsn,
    computed_field,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="smart_solutions/.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    MYSQL_SERVER: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = ""
    ALLOWED_TAGS: list[str] = ["detection", "segmentation", "classification", "tracking"]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MultiHostUrl.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_SERVER,
            port=self.MYSQL_PORT,
            path=self.MYSQL_DB,
        )


settings = Settings()
