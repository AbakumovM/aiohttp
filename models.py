from typing import Type

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import EmailType

Base = declarative_base()


class Ads(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    autor = Column(Integer, ForeignKey("ads_users.id", ondelete="CASCADE"))


class User(Base):
    __tablename__ = "ads_users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    password = Column(String(60), nullable=False)
    registration_time = Column(DateTime, server_default=func.now())


ORM_MODEL_CLS = Type[User] | Type[Ads]
ORM_MODEL = User | Ads
