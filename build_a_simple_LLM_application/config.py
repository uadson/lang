from decouple import config


class Settings:
    GOOGLE_API_KEY: str = config("GOOGLE_API_KEY")
    LANGSMITH_API_KEY: str = config("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT: str = config("LANGSMITH_PROJECT")
    LANGSMITH_TRACING: bool = config("LANGSMITH_TRACING")


settings: Settings = Settings()
