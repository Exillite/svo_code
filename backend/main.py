from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import os
import aiofiles

from pydantic import BaseModel
from typing import Optional, List

import uvicorn
from contextlib import asynccontextmanager

from mangodm import connect_to_mongo, close_mongo_connection, db

from models import User, Bio, Project, Work

import datetime
import time

from fastapi.responses import FileResponse


MONGODB_CONNECTION_URL = "mongodb://svodb"
DATABASE_NAME = "test_database"


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # execute when app is loading
    time.sleep(10)
    print("Loading app")
    await connect_to_mongo(MONGODB_CONNECTION_URL, DATABASE_NAME)
    print("Connected to mongo")
    yield
    # execute when app is shutting down
    print("Close db connection")
    close_mongo_connection()


app = FastAPI(lifespan=app_lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class UserCreateS(BaseModel):
    tg_id: int

@app.post("/api/user")
async def create_user(data: UserCreateS):
    new_user = User(tg_id=data.tg_id)
    await new_user.create()
    return {"status": "OK"}

class BioCreateS(BaseModel):
    tg_id: int
    name: str

@app.post("/api/bio")
async def creat_bio(data: BioCreateS):
    user = await User.get(tg_id=data.tg_id)
    if not user:
        return
    new_bio = Bio(name=data.name, user_id=user.id)
    await new_bio.create()
    user.bio_id = new_bio.id
    await user.update()
    return {"status": "OK"}



class BioAddSocialS(BaseModel):
    tg_id: int
    social: List[str]

@app.post("/api/bio/social")
async def bio_add_social(data: BioAddSocialS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return

    bio.social = data.social
    await bio.update()
    return {"status": "OK"}



class BioAddSocialS(BaseModel):
    tg_id: int
    social: List[str]

@app.post("/api/bio/social")
async def bio_add_social(data: BioAddSocialS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return

    bio.social = data.social
    await bio.update()
    return {"status": "OK"}


class BioAddDescriptionS(BaseModel):
    tg_id: int
    description: str

@app.post("/api/bio/description")
async def bio_add_description(data: BioAddDescriptionS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    bio.description = data.description
    await bio.update()
    return {"status": "OK"}


class BioAddProfS(BaseModel):
    tg_id: int
    prof: List[str]

@app.post("/api/bio/prof")
async def bio_add_prof(data: BioAddProfS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    bio.prof = data.prof
    await bio.update()
    return {"status": "OK"}


class BioAddTagsS(BaseModel):
    tg_id: int
    tags: List[str]

@app.post("/api/bio/tags")
async def bio_add_tags(data: BioAddTagsS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    bio.tags = data.tags + bio.prof
    await bio.update()
    return {"status": "OK"}


class BioAddMediaS(BaseModel):
    tg_id: int
    media_type: str # None / Image / Audio / Video / Links
    media: List[str]

@app.post("/api/bio/media")
async def bio_add_tags(data: BioAddMediaS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    bio.media_type = data.media_type
    bio.media = bio.media
    await bio.update()
    return {"status": "OK"}


class BioAddBackgroundS(BaseModel):
    tg_id: int
    background: str

@app.post("/api/bio/background")
async def bio_set_background(data: BioAddBackgroundS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    bio.background = data.background
    await bio.update()
    return {"status": "OK"}


class SetActiveBioS(BaseModel):
    tg_id: int
    is_active: bool

@app.post("/api/bio/active")
async def set_bio_active(data: SetActiveBioS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    bio.is_active = data.is_active
    await bio.update()
    return {"status": "OK"}


FILES_PATH = '/upload_files/'


def make_unique_filename(filename):
    """
    Given a filename, returns a unique filename by appending a number to the end of the filename
    if a file with that name already exists.
    """
    filename = filename.lower().replace(" ", "_")
    if not os.path.exists(filename):
        # If the filename doesn't exist, it's already unique
        return filename

    # If the filename exists, add a number to the end to make it unique
    i = 1
    while True:
        new_filename = f"{os.path.splitext(filename)[0]}_{i}{os.path.splitext(filename)[1]}"
        if not os.path.exists(new_filename):
            return new_filename
        i += 1


@app.post("/api/files/upload")
async def upload_file(files: List[UploadFile]):
    try:
        file_names = []
        for in_file in files:
            new_file_name = make_unique_filename(in_file.filename)
            out_file_path = FILES_PATH + new_file_name
            async with aiofiles.open(out_file_path, 'wb') as out_file:
                content = await in_file.read()  # async read
                await out_file.write(content)  # async write
            file_names.append(new_file_name)

        return {"status": 200, "files": file_names}
    except Exception as e:
        return {"status": 500, "error": str(e)}


@app.post("/api/files/load/{file_name}", response_class=FileResponse)
async def load_file(file_name: str):
    try:
        return FileResponse(FILES_PATH + file_name)
    except Exception as e:
        print(str(e))


class GetBioS(BaseModel):
    tg_id: int

@app.post("/api/bio/get")
async def get_bio(data: GetBioS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    bio = await Bio.get(id=user.bio_id)
    if not bio:
        return
    
    return bio.to_response()


async def get_workers_by_tags(tags: List[str]):
    cursor = db.db[Bio.Config.collection_name].find({"tags": {"$in": tags}})
    models = []
    
    async for document in cursor:
        tmp = await Bio.document_to_model(document)
        models.append((len(set(tags) & set(tmp.tags)), tmp.user_id))
        
    models = sorted(models, key=lambda x: x[0])
    
    ret = []
    for model in models:
        ret.append(model[1])

    return ret            


async def get_tags_from_description(description: str) -> List[str] | str | None:
    return []



class CreateProkectS(BaseModel):
    tg_id: str
    description: str

@app.post("/api/project/create")
async def create_project(data: CreateProkectS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    
    tgs = await get_tags_from_description(data.description)
    
    if tgs is None:
        return {"status": "retry"}
    elif isinstance(tgs, str):
        return {"status": "qestions", "text": tgs}
    elif isinstance(tgs, list):
        workers_ids = await get_workers_by_tags(tgs)
        new_pjct = Project(customer_id=user.id, description=data.description, workers_is=workers_ids, tags=tgs)
        await new_pjct.create()
        
        
        workers_tg_ids = []
        for wid in workers_ids:
            worker = await User.get(id=wid)
            if not worker:
                continue
            workers_tg_ids.append(worker.tg_id)
        

        return {"status": "OK", "workers_ids": workers_tg_ids}


class CreateWorkS(BaseModel):
    project_id: str
    tg_id: int
    chat_id: int

@app.post("/api/work/create")
async def create_work(data: CreateWorkS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    
    project = await Project.get(id=data.project_id)
    
    new_work = Work(customer_id=project.customer_id, worker_id=data.tg_id, chat_id=data.chat_id)
    await new_work.create()
    
    await project.delete()

    return "OK"


class AddContractS(BaseModel):
    chat_id: int
    days: int
    price: int
    description: str
    
@app.post("/api/works/contract")
async def add_contract(data: AddContractS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    
    work = await Work.get(chat_id=data.chat_id)
    if not work:
        return
    
    work.days = data.days
    work.price = data.price
    work.description = data.description
    work.is_contracted = True
    await work.update()
    
    return "OK"


@app.post("/api/works/contract/delete/{chat_id}")
async def add_contract(data: AddContractS):
    user = await User.get(tg_id=data.tg_id)
    if not user or not user.bio_id:
        return
    
    work = await Work.get(chat_id=data.chat_id)
    if not work:
        return
    
    await work.delete()
    
    return "OK"