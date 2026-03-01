from enum import StrEnum


class Environment(StrEnum):
    """Application environment"""

    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
