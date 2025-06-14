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

async def Logger(user: str, action: str, GUID: str):
    with open("logs.txt", "a") as f:
        f.write(f"{GUID} | {user} has {action}\n")

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
    
    if db_post.Name == "" or db_post.Description == "" or db_post.Stage == "" or db_post.Founder == "" or db_post.Field == "":
        return "Error, please fill in all fields"
    else:
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        await Logger("Connor", "created a startup", "7171f1b1-ea0a-44c1-a134-f3152cb4aeb5")
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

    if db_post.CompanyName == "" or db_post.JobTitle == "" or db_post.JobDescription == "" or db_post.StartDate == "":
        return "Error, please fill in all fields"
    else:
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        await Logger("Connor", "created a job role", "ce32a32a-61dc-458a-a443-5ff00fd6cc72")
        return "Success"

@app.delete("/deleteStartUp/{id}", response_model=None)
async def delete_StartUp(id: int, db: db_dependency):

    db.query(dbSchema.startUpModel).filter(dbSchema.startUpModel.id == id).delete()
    db.commit()
    await Logger("Connor", "deleted a startup", "df748e6f-2e18-4e9a-8b76-2a56ffe09e5b")
    return "Success"

@app.delete("/deleteJobRole/{id}", response_model=None)
async def delete_JobRole(id: int, db: db_dependency):

    db.query(dbSchema.JobRole).filter(dbSchema.JobRole.id == id).delete()
    db.commit()
    await Logger("Connor", "deleted a job role", "e962345a-f61e-4cef-b663-280aaec107a6")
    return "Success"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)