from typing import Dict

from aiohttp.helpers import BasicAuth
from fastapi.security.utils import get_authorization_scheme_param
from requests.auth import AuthBase

from .aad_autherror import AuthError


class AuthToken(AuthBase, BasicAuth):
    def __init__(
        self,
        access_token: str = None,
        id_token: str = None,
        refresh_token: str = None,
        client_info: str = None,
        token: Dict[str, str] = None,
    ):

        self.access_token = access_token
        self.id_token = id_token
        self.client_info = client_info
        self.refresh_token = refresh_token

        if token:
            if "access_token" in token:
                self.access_token = token["access_token"]
            if "id_token" in token:
                self.id_token = token["id_token"]
            if "client_info" in token:
                self.client_info = token["client_info"]
            if "refresh_token" in token:
                self.refresh_token = token["refresh_token"]

        if self.access_token is None:
            raise AuthError(
                "access_token_empty", "No access token in the BearerAuth instance"
            )

        if self.access_token.lower().startswith("bearer"):
            _, self.access_token = get_authorization_scheme_param(self.access_token)

    # Used by BasicAuth
    def __new__(
        cls,
        login: str = "",
        password: str = "",
        encoding: str = "latin1",
        *args,
        **kwargs,
    ) -> BasicAuth:
        # even if not used, mandatory to be sure instance is not returning False
        login = login if login is not None and login != "" else "unused"
        return super().__new__(cls, login, password, encoding)

    # Used by BasicAuth
    def encode(self) -> str:
        return f"Bearer {self.access_token}"

    # User by AuthBase
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.access_token
        return r
