from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_app_url: str
    login_url: str
    sign_up_url: str
    email: str
    password: str