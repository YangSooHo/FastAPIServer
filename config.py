from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # .env 미적용 시 아래와 같이 직접 설정
    # DB_USER: str = "postgres"
    # DB_PASSWORD: str = "test123!@#"
    # DB_HOST: str = "localhost"
    # DB_PORT: int = 5432
    # DB_NAME: str = "fast_api"

    # DATABASE_URL: str = (
    #     f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # )

    # 함수지만 속성처럼 읽을 수 있게 해줌 ex) settings.DATABASE_URL() => settings.DATABASE_URL
    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"  # 환경 변수 파일 (.env) 자동으로 읽음

settings = Settings()