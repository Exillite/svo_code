from mangodm import Document
from typing import List, Optional
from datetime import datetime

class User(Document):
    tg_id: int
    bio_id: Optional[str]

    class Config:
        collection_name = "Users"


class Bio(Document):
    is_active: bool = False
    name: Optional[str] = None
    social: Optional[List[str]]
    description: Optional[str]
    prof: Optional[List[str]]
    tags: Optional[List[str]]
    media_type: Optional[str]
    media: Optional[List[str]]
    
    background: Optional[str]

    class Config:
        collection_name = "Bios"

User.register_collection()
Bio.register_collection()
