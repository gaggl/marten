from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import (
    Column,
    Float,
    String,
    Integer,
)

Base = declarative_base()

class HttpStatusCodes(Base):
    __tablename__ = 'httpStatusCodes'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(80))
    status_code = Column(Integer())
    probability = Column(Float())

    @classmethod
    def from_tuple(cls, data):
        return cls(message=data[0], status_code=data[1], probability=data[2])

    @classmethod
    def bootstrap(self, db, data):
        db.create_all()
        if not db.session.query(HttpStatusCodes).count():
            for item in data:
                db.session.add(HttpStatusCodes.from_tuple(item))
            db.session.commit()
