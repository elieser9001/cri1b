from app import create_app
from app.database.database import init_db
# from sqlalchemy.orm import Session
# from app.database.database import SessionLocal, engine
# from app.database import crud, models

# models.Base.metadata.create_all(bind=engine)

# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

init_db()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

from app.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()