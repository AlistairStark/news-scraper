from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt

from app import settings


@dataclass
class TokenData:
    identity: str
    expiry: datetime


class TokenService:
    ALGORITHM = "HS256"

    def create_token(self, identity: str) -> str:
        expiry = datetime.now(timezone.utc) + timedelta(hours=4)
        return jwt.encode(
            {"identity": identity, "expiry": expiry.isoformat()},
            settings.TOKEN_SECRET,
            algorithm=self.ALGORITHM,
        )

    def decode_token(self, encoded_token: str) -> TokenData:
        token = jwt.decode(
            encoded_token, settings.TOKEN_SECRET, algorithms=[self.ALGORITHM]
        )
        return TokenData(
            identity=token["identity"], expiry=datetime.fromisoformat(token["expiry"])
        )
