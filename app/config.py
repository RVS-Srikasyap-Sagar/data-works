import os

class Settings:
    @property
    def ai_proxy_token(self):
        return os.getenv("AIPROXY_TOKEN")

settings = Settings()
