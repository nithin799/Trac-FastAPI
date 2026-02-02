from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


db_url = "postgresql://postgres:root@localhost:5432/trac"  #url
engine = create_engine(db_url)     # which database should be choosen

session = sessionmaker(autocommit = False,autoflush = False,bind = engine)   #database connection  