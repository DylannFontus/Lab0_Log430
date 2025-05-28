from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:password@mysql:3306/magasin"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
