from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.db.tasks import Base


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    created_by = relationship("User", back_populates="blog")


class User(Base):
    __tablename__ = 'users'

    id= Column(Integer, primary_key=True, index=True )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    blog = relationship("Blog", back_populates="created_by")

class People(Base):
    __tablename__ = 'people'

    id= Column(Integer, primary_key=True, index=True )
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)

    blog = relationship("Blog", back_populates="created_by")