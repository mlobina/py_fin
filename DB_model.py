
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from VK_DB_connections import DataBaseConnection



session = DataBaseConnection().session
engine = DataBaseConnection().engine
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, unique=True)


class DatingUser(Base):
    __tablename__ = 'dating_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    city = Column(String)
    link = Column(String)
    status = Column(Integer)
    id_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))


class Photos(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    link_photo = Column(String)
    count_likes = Column(Integer)
    id_dating_user = Column(Integer, ForeignKey('dating_user.id', ondelete='CASCADE' ))


class BlackList(Base):
    __tablename__ = 'black_list'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    city = Column(String)
    link = Column(String)
    status = Column(Integer)
    link_photo = Column(String)
    count_likes = Column(Integer)
    id_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))


if __name__ == '__main__':
    Base.metadata.create_all(engine)








