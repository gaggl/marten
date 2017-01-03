from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import (
    Column,
    String,
    Integer,
)

Base = declarative_base()

class HttpStatusCodes(Base):
    __tablename__ = 'httpStatusCodes'
    _id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(80))
    percentage = Column(Integer())
    status_code = Column(Integer())

    @classmethod
    def from_tuple(cls, data):
        return cls(message=data[0], percentage=data[2], status_code=data[1])

    @classmethod
    def bootstrap(self, db, data):
        db.create_all()
        if not db.session.query(HttpStatusCodes).count():
            for item in data:
                db.session.add(HttpStatusCodes.from_tuple(item))
            db.session.commit()
