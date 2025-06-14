from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from databaseConfig import Base

class startUpModel(Base):
    __tablename__ = "StartUps"

    id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Description = Column(String)
    Stage = Column(String)
    isRecruiting = Column(Boolean)
    Founder = Column(String)
    Field = Column(String)

    class Config:
        orm_mode = True

class JobRole(Base):
    __tablename__ = "JobRoles"
    id = Column(Integer, primary_key=True)
    CompanyName = Column(String, ForeignKey("StartUps.Name"))
    JobTitle = Column(String)
    JobDescription = Column(String)
    StartDate = Column(String)

    class Config:
        orm_mode = True