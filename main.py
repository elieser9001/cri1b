from app import create_app
from app.database.database import init_db

init_db()
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

from app.database.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()