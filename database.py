from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL='postgresql://imrane:t6p78CVHWVBM09iEt3IbI9YEMmoGTBfU@dpg-ci8rn0tgkuvmfnsaa9j0-a.oregon-postgres.render.com/snappyshop'


#connect 
database_engine = create_engine(DATABASE_URL)

# equivalent à un "cursor"
SessionTemplate = sessionmaker(bind=database_engine, autocommit=False, autoflush=False)

def get_cusor():
    db= SessionTemplate()
    try:
        yield db
    finally:
        db.close()
