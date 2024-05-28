import datetime
import uuid
from pydantic import BaseModel


class EmailConfirmCodeBase(BaseModel):
    user_id: uuid.UUID
    code: int


class EmailConfirmCodeResponse(EmailConfirmCodeBase):
    id: uuid.UUID
    created_at: datetime.datetime
