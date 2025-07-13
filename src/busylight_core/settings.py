"""busylight_core Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for busylight_core."""

    model_config = SettingsConfigDict(
        env_prefix="BUSYLIGHT_CORE",
        env_file=".env-busylight_core",
    )
    debug: bool = False
