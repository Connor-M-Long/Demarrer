from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from databaseConfig import Base

class startUpModel(Base):
    __tablename__ = "StartUps"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    isRecruiting = Column(Boolean)

    class Config:
        orm_mode = True

class JobRole(Base):
    __tablename__ = "JobRoles"
    id = Column(Integer, primary_key=True)
    CompanyName = Column(String, ForeignKey("StartUps.name"))
    JobTitle = Column(String)
    JobDescription = Column(String)
    StartDate = Column(String)

    class Config:
        orm_mode = True