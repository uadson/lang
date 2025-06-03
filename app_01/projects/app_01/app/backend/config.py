from decouple import config


class Settings:
    PROVIDER_API_KEY: str = config("PROVIDER_API_KEY")
    LLM_MODEL: str = config("LLM_MODEL")
    MODEL_PROVIDER: str = config("MODEL_PROVIDER")


settings: Settings = Settings()
