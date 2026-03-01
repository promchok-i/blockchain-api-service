from pydantic import BaseModel
from typing import List


class DocumentInput(BaseModel):
    document_id: str
    issuer_id: str
    holder_id: str
    hashed_content: str
    is_active: bool

class DocumentQueryInput(BaseModel):
    document_ids: List[str]
