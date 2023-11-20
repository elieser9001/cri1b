from app.database.database import db_session
from app.database.models import  License
from datetime import datetime
import uuid
    
def get_license(key: str):
    try:
        result = License.query.filter(License.key == key).one()
    except:
        result = None
        
    return result

def create_license(
    # extension_id: str,
    # device_id: str,
    # key: str,
    name: str,
    lastname: str,
    email: str,
    phone_number: str,
    expired_time: str
):  
    #  "%Y-%m-%d %I:%M:%S %p"
    expired_time = datetime.strptime(expired_time, "%d-%m-%Y %I:%M:%S %p")
    key = str(uuid.uuid4())
    
    license = License(
        # extension_id,
        # device_id,
        key=key,
        name=name,
        lastname=lastname,
        email=email,
        phone_number=phone_number,
        expired_time=expired_time
     )
    
    db_session.add(license)
    db_session.commit()
