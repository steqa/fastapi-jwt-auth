from datetime import datetime, timedelta, UTC
import uuid

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.database import Base
from src.config import settings


class EmailConfirmCode(Base):
    __tablename__ = 'email_confirm_code'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), unique=True)
    code = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    expired_at = Column(
        DateTime,
        default=datetime.now(UTC) + timedelta(
            minutes=settings.EMAIL_CONFIRM_CODE_EXPIRE_MINUTES
        )
    )
