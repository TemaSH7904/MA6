from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class MessageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    sender_name: str
    receiver_name: str
    datetime: datetime
    text: str