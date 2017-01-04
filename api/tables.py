from sqlalchemy.ext.declarative import declarative_base
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
    status_code = Column(Integer())
    payload = Column(String(80))
    probability = Column(Float())
    count = Column(Integer, server_default='0')

    @classmethod
    def from_tuple(cls, data):
        return cls(status_code=data['status_code'], payload=data['payload'], probability=data['probability'])

    @classmethod
    def bootstrap(self, db, data):
        db.create_all()
        if not db.session.query(HttpStatusCodes).count():
            for item in data:
                db.session.add(HttpStatusCodes.from_tuple(item))
            db.session.commit()
