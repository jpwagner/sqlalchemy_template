from sqlalchemy import MetaData, Column,\
					Integer, String, Text, DateTime, Date, PickleType,\
					create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates
from sqlalchemy.sql import func

import settings

Base = declarative_base()

class CommonBase(Base):
	__abstract__ = True

	id = Column(Integer, primary_key=True)
	created_on = Column(DateTime, default=func.now())
	updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

	@classmethod
	def create_table(self):
		engine = create_db_engine()
		self.__table__.create(engine)	
		return None

	@classmethod
	def drop_table(self):
		engine = create_db_engine()
		self.__table__.drop(engine)
		return None


class SomeTable(CommonBase):
	__tablename__ = 'some_table'

	field1 = Column(Integer, nullable=True)
	field2 = Column(String(255), nullable=True)


def create_db_engine(db=settings.DB):
	if db['ENGINE']=='sqlite':
		from sqlite3 import dbapi2 as sqlite
		return create_engine('sqlite+pysqlite:///%s' % (db['NAME']), module=sqlite)

	engine = create_engine('%s://%s:%s@%s/%s' \
			% (db['ENGINE'], db['USER'], db['PASSWORD'], db['HOST'], db['NAME'])\
			, use_native_unicode=False) #, client_encoding='utf8')
	return engine

def create_db_session(db=settings.DB):
	engine = create_db_engine(db)
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

def end_db_session(session):
	session.commit()
	session.close()
	return
