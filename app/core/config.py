"""
Application Configuration
-------------------------
Central configuration and settings for the application.
"""

import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server
    app_name: str = "Gmail Cleaner"
    app_version: str = "1.0.0"
    debug: bool = False
    port: int = 8766
    oauth_port: int = 8767
    oauth_external_port: int | None = Field(
        default=None,
        description="External port for OAuth redirect URI (when different from oauth_port, e.g., Docker port mapping)",
    )

    # Auth
    web_auth: bool = Field(
        default=False,
        description="Enable web-based authentication mode",
    )
    oauth_host: str = Field(
        default="localhost",
        description="Custom host for OAuth redirect (e.g., your domain or IP)",
    )

    @field_validator("web_auth", mode="before")
    @classmethod
    def validate_web_auth(cls, v) -> bool:
        """Convert string environment variable to boolean (case-insensitive)."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            normalized = v.lower().strip()
            return normalized in ("true", "1", "yes", "on")
        return bool(v)

    credentials_file: str = "credentials.json"
    token_file: str = "token.json"

    def __init__(self, **kwargs):
        """Initialize settings and auto-detect data directory for token persistence."""
        super().__init__(**kwargs)
        # Auto-detect /app/data directory in Docker and use it for token_file
        # This allows token.json to persist across container restarts
        if os.path.exists("/app/data") and os.path.isdir("/app/data"):
            # Normalize the base directory path
            base_dir = os.path.abspath(os.path.realpath("/app/data"))

            if os.path.isabs(self.token_file):
                # If token_file is absolute, verify it's within /app/data
                resolved_path = os.path.abspath(os.path.realpath(self.token_file))
                if (
                    not resolved_path.startswith(base_dir + os.sep)
                    and resolved_path != base_dir
                ):
                    # Absolute path outside /app/data - use safe fallback
                    self.token_file = os.path.join(
                        base_dir, os.path.basename(self.token_file)
                    )
                else:
                    # Valid absolute path within /app/data
                    self.token_file = resolved_path
            else:
                # Relative path - join and validate
                candidate_path = os.path.join(base_dir, self.token_file)
                resolved_path = os.path.abspath(os.path.realpath(candidate_path))

                # Verify resolved path is within base_dir (prevents path traversal)
                if (
                    not resolved_path.startswith(base_dir + os.sep)
                    and resolved_path != base_dir
                ):
                    # Path traversal detected - use safe fallback with basename only
                    self.token_file = os.path.join(
                        base_dir, os.path.basename(self.token_file)
                    )
                else:
                    # Safe path - use resolved path
                    self.token_file = resolved_path

    # Gmail API
    scopes: list[str] = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.modify",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Global settings instance
settings = Settings()
