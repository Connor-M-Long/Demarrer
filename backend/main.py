import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
from databaseConfig import engine, SessionLocal
import dbSchema

class StartUp(BaseModel):
    Name: str
    Description: str
    Stage: str
    isRecruiting: bool
    Founder: str
    Field: str

class JobRole(BaseModel):
    CompanyName: str
    JobTitle: str
    JobDescription: str
    StartDate: str

app = FastAPI()
dbSchema.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

memory_db_startup = {"startup": []}
memory_db_jobroles = {"jobroles": []}

@app.get("/startups", response_model=None)
async def get_StartUps(db: db_dependency):

    memory_db_startup["startup"].clear()
    result = db.query(dbSchema.startUpModel).all()

    for startUp in result:
        memory_db_startup["startup"].append(startUp)

    return memory_db_startup

@app.post("/createStartUp", response_model=None)
async def add_StartUp(request: StartUp, db: db_dependency):

    db_post = dbSchema.startUpModel(
        Name = request.Name,
        Description = request.Description,
        isRecruiting = request.isRecruiting,
        Stage=request.Stage,
        Founder=request.Founder,
        Field=request.Field)

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return "Success"

@app.get("/jobroles/{companyname}", response_model=None)
async def get_JobRoles(companyname: str, db: db_dependency):

    memory_db_jobroles["jobroles"].clear()
    result = db.query(dbSchema.JobRole).filter(dbSchema.JobRole.CompanyName == companyname).all()

    for role in result:
        memory_db_jobroles["jobroles"].append(role)

    return memory_db_jobroles

@app.post("/createJobRole", response_model=None)
async def add_JobRole(request: JobRole, db: db_dependency):

    db_post = dbSchema.JobRole(
        CompanyName = request.CompanyName,
        JobTitle = request.JobTitle,
        JobDescription = request.JobDescription,
        StartDate = request.StartDate
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return "Success"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)