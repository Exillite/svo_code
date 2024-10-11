from mangodm import Document
from typing import List, Optional
from datetime import datetime

class User(Document):
    tg_id: int
    bio_id: Optional[str]
    done_works: int

    class Config:
        collection_name = "Users"


class Bio(Document):
    user_id: str
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


class Project(Document):
    customer_id: str
    description: str
    tags: Optional[List[str]]
    workers_is: Optional[List[str]]
    
    class Config:
        collection_name = "Projects"
    
class Work(Document):
    customer_id: str
    worker_id: str
    is_contracted: bool = False
    days: Optional[int]
    price: Optional[int]
    description: Optional[str]
    chat_id: int
    
    class Config:
        collection_name = "Works"


User.register_collection()
Bio.register_collection()
Project.register_collection()
Work.register_collection()
